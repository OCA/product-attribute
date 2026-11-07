# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=translation-not-lazy,prefer-env-translation,no-name-in-module,missing-class-docstring,abstract-method,invalid-name

import logging
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProductCategoryHsMapping(models.Model):
    _name = "product.category.hs.mapping"
    _description = "HS Code → Product Category Mapping"
    _order = "specificity desc, sequence, id"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        help=(
            "Human-readable label combining the HS pattern and the "
            "category — used in Many2one displays and audit trails."
        ),
    )
    hs_code_pattern = fields.Char(
        required=True,
        help=(
            "HS tariff code pattern. Treated as a prefix at lookup "
            "time — a rule with literal '84312000' matches both "
            "'84312000' and '8431200080' (longer national tariff "
            "lines roll up to the same chapter / subheading). The "
            "trailing '*' is purely visual; '84312000' and '84312000*' "
            "behave identically. Longest literal wins."
        ),
    )
    category_id = fields.Many2one(
        comodel_name="product.category",
        required=True,
        ondelete="cascade",
        help="Target product category for products matching this pattern.",
    )
    sequence = fields.Integer(
        default=10,
        help=(
            "Tiebreaker among same-specificity rules — lower wins. "
            "Specificity (longer pattern → higher) takes precedence."
        ),
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        help=(
            "Restrict this rule to a specific company. Empty = applies "
            "to all companies. Multi-company customers can ship "
            "different mapping tables per legal entity."
        ),
    )
    specificity = fields.Integer(
        compute="_compute_specificity",
        store=True,
        index=True,
        help=(
            "Length of the literal portion of the pattern (the part "
            "before any '*'). Used to order matches longest-first so "
            "an exact code beats a prefix wildcard."
        ),
    )
    active = fields.Boolean(default=True)
    intrastat_description = fields.Char(
        compute="_compute_intrastat_description",
        help=(
            "Plain-language description of what the rule's HS-code "
            "pattern actually covers, looked up against the installed "
            "``account.intrastat.code`` records. Lets a buyer eyeball "
            "whether ``8539299*`` mapped to 'Hydraulics' is wrong "
            "(it is — it's Filament lamps) without consulting a "
            "tariff manual. Computed, not stored — refreshes when "
            "the pattern changes or new intrastat codes get loaded."
        ),
    )

    @api.depends("hs_code_pattern")
    def _compute_intrastat_description(self):
        # Resolve via the same prefix logic the matcher itself uses.
        # Cheap when account_intrastat isn't installed: env reference
        # raises KeyError, which we catch and skip.
        try:
            IntrastatCode = self.env["account.intrastat.code"].sudo()
        except KeyError:
            for rec in self:
                rec.intrastat_description = ""
            return
        # The 3-tier lookup below is unreachable in this module's
        # CI because ``account.intrastat.code`` lives in OCA's
        # ``account_intrastat`` (a separate project). Adding it as
        # a manifest dep would cross OCA-project boundaries for a
        # purely cosmetic field. The KeyError early-return above
        # handles the common case (matcher installed without
        # ``account_intrastat``); the lookup below kicks in for
        # users who do have it installed alongside. Excluded from
        # coverage explicitly.
        for rec in self:  # pragma: no cover
            literal = (rec.hs_code_pattern or "").rstrip("*")
            if not literal:
                rec.intrastat_description = ""
                continue
            # 1. Exact match wins outright.
            exact = IntrastatCode.search([("code", "=", literal)], limit=1)
            if exact:
                rec.intrastat_description = exact.description or ""
                continue
            # 2. Shortest intrastat code that EXTENDS the pattern's
            #    literal — gives a representative leaf description.
            #    e.g. literal=``8539299`` matches ``85392998`` (the
            #    8-digit subheading "Filament lamps...").
            extending = IntrastatCode.search(
                [("code", "=like", literal + "%")],
                order="code",
                limit=1,
            )
            if extending:
                rec.intrastat_description = (
                    f"({extending.code}) {extending.description or ''}".strip()
                )
                continue
            # 3. Shortest intrastat code the pattern itself EXTENDS —
            #    e.g. literal=``8431200080`` (10-digit national tariff
            #    line) extends ``84312000`` (8-digit subheading) which
            #    has the description we want.
            for length in (10, 8, 6, 4, 2):
                if length >= len(literal):
                    continue
                parent = IntrastatCode.search(
                    [("code", "=", literal[:length])], limit=1
                )
                if parent:
                    rec.intrastat_description = (
                        f"({parent.code}) {parent.description or ''}".strip()
                    )
                    break
            else:
                rec.intrastat_description = ""

    @api.constrains("hs_code_pattern", "company_id")
    def _check_pattern_company_unique(self):
        """Reject duplicate (pattern, company_id) — implemented in
        Python rather than via SQL ``UNIQUE`` because PostgreSQL's
        default ``UNIQUE`` semantic treats NULL company_ids as
        distinct, which would let two global rules for the same
        pattern coexist (defeating the constraint). PostgreSQL 15+
        offers ``UNIQUE NULLS NOT DISTINCT`` but that path needs
        more careful Odoo-version gating; the Python check is
        portable and clear."""
        for rec in self:
            domain = [
                ("hs_code_pattern", "=", rec.hs_code_pattern),
                ("id", "!=", rec.id),
            ]
            if rec.company_id:
                domain.append(("company_id", "=", rec.company_id.id))
            else:
                domain.append(("company_id", "=", False))
            if self.search_count(domain):
                raise ValidationError(
                    _(
                        "An HS-code mapping rule for pattern "
                        "'%(pat)s' and the same company scope already "
                        "exists. Patterns must be unique per company "
                        "(or globally, when no company is set)."
                    )
                    % {"pat": rec.hs_code_pattern}
                )

    @api.depends("hs_code_pattern", "category_id")
    def _compute_name(self):
        for rec in self:
            if rec.hs_code_pattern and rec.category_id:
                rec.name = f"{rec.hs_code_pattern} → {rec.category_id.display_name}"
            else:
                rec.name = rec.hs_code_pattern or ""

    @api.depends("hs_code_pattern")
    def _compute_specificity(self):
        for rec in self:
            pat = rec.hs_code_pattern or ""
            # Specificity = literal-prefix length. "8421230090" → 10,
            # "8421*" → 4, "*" → 0. Longest literal wins at lookup.
            literal = pat.split("*", 1)[0]
            rec.specificity = len(literal)

    @api.constrains("hs_code_pattern")
    def _check_pattern_shape(self):
        # Allow digits and at most one trailing '*'. HS codes are
        # numeric (typically 6/8/10 digits); accept anything in between
        # so partial chapter prefixes like '84' work.
        # A bare ``*`` is a deliberate catch-all (specificity 0,
        # last-resort match) — also allowed.
        for rec in self:
            pat = (rec.hs_code_pattern or "").strip()
            if not pat:
                raise ValidationError(_("HS code pattern is required."))
            if pat == "*":
                # Bare catch-all — accepted, no further checks.
                continue
            literal = pat.rstrip("*")
            if not literal:
                raise ValidationError(
                    _(
                        "HS code pattern must contain at least one digit "
                        "before any '*' wildcard."
                    )
                )
            if not re.fullmatch(r"\d+", literal):
                raise ValidationError(
                    _(
                        "HS code pattern '%(pat)s' must contain only "
                        "digits (and an optional trailing '*'); got "
                        "non-digit characters."
                    )
                    % {"pat": pat}
                )
            # Reject internal '*' — only trailing wildcard supported.
            if "*" in pat[:-1]:
                raise ValidationError(
                    _(
                        "HS code pattern '%(pat)s' has a '*' that isn't "
                        "the last character. Only trailing wildcard is "
                        "supported (e.g. '8421*'). Use a longer literal "
                        "prefix instead."
                    )
                    % {"pat": pat}
                )

    @api.model
    def _get_category_for_hs_code(self, hs_code, company=None):
        """Return the best-matching ``product.category`` for the given
        HS code, or an empty recordset.

        Matching: every rule's literal (the part before any ``*``) is
        treated as a prefix. HS codes are hierarchical — a 6-digit
        chapter heading rolls up everything under it (8-digit
        subheading, 10-digit national tariff line, ...) — so a rule
        with literal ``"84312000"`` should naturally match an input
        of ``"8431200080"``. The trailing ``*`` is purely visual: a
        rule with or without it matches the same set of inputs. Rules
        are ordered by specificity (literal length, longest first)
        then by sequence, so the most specific rule wins.

        Company scoping: rules with ``company_id`` set match only when
        ``company`` matches; rules with no ``company_id`` apply to all
        companies. When ``company`` is None, falls back to
        ``self.env.company``.

        Used by EDI / supplier-integration glue to auto-categorise
        newly imported products. Safe to call with garbage input —
        empty / non-digit codes return an empty category, never raise.
        Logs at INFO level when a non-empty input doesn't match any
        rule so previously-silent gaps surface in the server log.
        """
        if not hs_code:
            return self.env["product.category"]
        # Strip whitespace and ensure pure digits before matching.
        # HS codes from external systems sometimes have dots / spaces.
        clean = re.sub(r"\D", "", hs_code)
        if not clean:
            return self.env["product.category"]
        company = company or self.env.company
        # Domain pulls only rules that could match: same company or
        # global. We then filter Python-side by prefix because SQL
        # LIKE on `hs_code_pattern LIKE '<prefix>%'` would be the
        # wrong direction (we want our code to start with the rule's
        # literal, not vice-versa).
        candidates = self.search(
            [
                ("active", "=", True),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", company.id),
            ],
            order="specificity desc, sequence, id",
        )
        for rule in candidates:
            literal = (rule.hs_code_pattern or "").rstrip("*")
            # Empty literal = bare ``*`` catch-all. Order is
            # specificity-desc so this rule sits last among
            # candidates; it only fires when nothing more specific
            # already matched and returned above.
            if not literal:
                return rule.category_id
            if clean.startswith(literal):
                return rule.category_id
        _logger.info(
            "[product.category.hs.mapping] no rule matched HS code %r "
            "(cleaned %r) for company %s — product left in default "
            "category. Add a mapping if this should auto-categorise.",
            hs_code,
            clean,
            company.display_name,
        )
        return self.env["product.category"]
