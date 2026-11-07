# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=abstract-method,translation-not-lazy,prefer-env-translation,no-name-in-module,invalid-name,protected-access,use-implicit-booleaness-not-comparison-to-zero

import logging

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """Adds the manual ``Apply HS Code → Category Mapping`` server
    action to ``product.template``. The mapping itself is defined in
    ``product.category.hs.mapping``; this method just wires the
    matcher to the per-product context-menu action so a buyer can
    debug, test, or selectively re-apply a rule against a specific
    product without going through the full Refresh-from-supplier
    flow.

    Lives in this module (not a downstream consumer) because it's
    the natural extension of the matcher — re-running the resolver
    against the product's own ``hs_code`` field.
    """

    _inherit = "product.template"

    def action_apply_hs_mapping(self):
        """Re-run the HS-code matcher against each selected product
        and write the result to ``categ_id``.

        Raises a ``UserError`` for SINGLE-product invocations when
        nothing happens (no HS code / no rule / already in matched
        category) so the buyer sees the cause directly. Multi-product
        invocations show a summary toast with the breakdown
        (updated / unchanged / skipped) and a ``soft_reload`` so the
        list refreshes without a manual F5.

        Permissions: relies on the standard ``product.template``
        write ACL — anyone with edit rights can re-categorise.
        Fine-grained "only purchasing" gating is left to the
        deployer via Odoo's standard record rules / group
        memberships, no need for our own ACL."""
        if not self:
            return False
        Mapping = self.env["product.category.hs.mapping"]
        updated = 0
        unchanged = 0
        skipped_no_code = 0
        skipped_no_rule = 0
        for tmpl in self:
            hs_code = (tmpl.hs_code or "").strip()
            if not hs_code:
                skipped_no_code += 1
                continue
            new_category = Mapping._get_category_for_hs_code(hs_code, tmpl.company_id)
            if not new_category:
                skipped_no_rule += 1
                continue
            if new_category == tmpl.categ_id:
                unchanged += 1
                continue
            old_category = tmpl.categ_id
            tmpl.categ_id = new_category
            tmpl.message_post(
                body=self.env._(
                    "Re-categorised via HS-code mapping: %(hs)s — %(old)s → %(new)s",
                    hs=hs_code,
                    old=old_category.display_name or "(unset)",
                    new=new_category.display_name,
                )
            )
            updated += 1
        # Single-product manual invocation: surface the "why nothing
        # happened" reason as a UserError so the buyer reads it
        # directly instead of a tucked-away notification toast.
        if len(self) == 1 and updated == 0:
            if skipped_no_code:
                raise UserError(
                    self.env._(
                        "Product %(name)s has no HS code set. "
                        "Fill ``hs_code`` first (Product form → "
                        "Purchase tab) or via TVH enrichment.",
                        name=self.display_name,
                    )
                )
            if skipped_no_rule:
                raise UserError(
                    self.env._(
                        "No HS-code mapping rule matches "
                        "%(hs)s for %(name)s. Add a rule in "
                        "Settings → Technical → Product Category "
                        "HS Mapping, or extend the parent prefix.",
                        hs=hs_code,
                        name=self.display_name,
                    )
                )
            if unchanged:
                raise UserError(
                    self.env._(
                        "Product %(name)s is already in the "
                        "matched category (%(cat)s).",
                        name=self.display_name,
                        cat=self.categ_id.display_name,
                    )
                )
        # Multi-product: summary toast + soft_reload to refresh the
        # list view in place.
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("HS Code Mapping"),
                "message": self.env._(
                    "%(updated)d re-categorised, %(unchanged)d "
                    "already correct, %(no_code)d without HS "
                    "code, %(no_rule)d with no matching rule.",
                    updated=updated,
                    unchanged=unchanged,
                    no_code=skipped_no_code,
                    no_rule=skipped_no_rule,
                ),
                "type": "success" if updated else "warning",
                "next": {"type": "ir.actions.client", "tag": "soft_reload"},
            },
        }
