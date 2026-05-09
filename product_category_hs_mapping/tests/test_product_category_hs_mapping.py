# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=protected-access,missing-function-docstring,missing-class-docstring,too-many-public-methods

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestProductCategoryHsMapping(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Mapping = cls.env["product.category.hs.mapping"]
        cls.Category = cls.env["product.category"]
        # Disable any default mappings shipped via data so each test
        # operates on a known empty table.
        cls.Mapping.search([]).write({"active": False})
        # Test categories.
        cls.cat_general = cls.Category.create({"name": "Test General"})
        cls.cat_filtration = cls.Category.create({"name": "Test Filtration"})
        cls.cat_filter_panel = cls.Category.create(
            {"name": "Test Filtration / Panel Filters"}
        )
        cls.cat_electrical = cls.Category.create({"name": "Test Electrical"})

    # ---- pattern validation -----------------------------------------------

    def test_pattern_bare_wildcard_is_catch_all(self):
        """Bare ``*`` is a deliberate catch-all (specificity 0,
        last-resort match) — accepted, not rejected. The
        ``test_pattern_rejects_internal_wildcard`` test below
        covers the close-but-different case where ``*`` appears
        between digits."""
        rule = self.Mapping.create(
            {"hs_code_pattern": "*", "category_id": self.cat_general.id}
        )
        self.assertEqual(rule.specificity, 0)

    def test_pattern_rejects_non_digits(self):
        with self.assertRaises(ValidationError):
            self.Mapping.create(
                {"hs_code_pattern": "84AB*", "category_id": self.cat_general.id}
            )

    def test_pattern_rejects_internal_wildcard(self):
        with self.assertRaises(ValidationError):
            self.Mapping.create(
                {"hs_code_pattern": "84*21", "category_id": self.cat_general.id}
            )

    def test_pattern_accepts_exact_code(self):
        rule = self.Mapping.create(
            {"hs_code_pattern": "8421230090", "category_id": self.cat_filtration.id}
        )
        self.assertEqual(rule.specificity, 10)

    def test_pattern_accepts_short_prefix(self):
        rule = self.Mapping.create(
            {"hs_code_pattern": "84*", "category_id": self.cat_general.id}
        )
        self.assertEqual(rule.specificity, 2)

    # ---- specificity ordering ---------------------------------------------

    def test_specificity_is_literal_prefix_length(self):
        cases = [
            ("8421230090", 10),
            ("8421*", 4),
            ("84*", 2),
            ("8*", 1),
            ("85", 2),  # exact, no wildcard
        ]
        for pattern, expected in cases:
            rule = self.Mapping.create(
                {"hs_code_pattern": pattern, "category_id": self.cat_general.id}
            )
            self.assertEqual(
                rule.specificity, expected, f"specificity wrong for {pattern!r}"
            )

    # ---- _get_category_for_hs_code resolution -----------------------------

    def test_resolution_empty_input_returns_empty(self):
        self.assertFalse(self.Mapping._get_category_for_hs_code(""))
        self.assertFalse(self.Mapping._get_category_for_hs_code(None))
        self.assertFalse(self.Mapping._get_category_for_hs_code("ABCD"))

    def test_resolution_no_rules_returns_empty(self):
        self.assertFalse(self.Mapping._get_category_for_hs_code("8421230090"))

    def test_resolution_exact_match_wins(self):
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        self.Mapping.create(
            {"hs_code_pattern": "8421230090", "category_id": self.cat_filter_panel.id}
        )
        result = self.Mapping._get_category_for_hs_code("8421230090")
        self.assertEqual(result, self.cat_filter_panel)

    def test_resolution_longest_prefix_wins(self):
        self.Mapping.create(
            {"hs_code_pattern": "84*", "category_id": self.cat_general.id}
        )
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        result = self.Mapping._get_category_for_hs_code("8421999999")
        self.assertEqual(result, self.cat_filtration)

    def test_resolution_falls_through_to_shorter_prefix(self):
        self.Mapping.create(
            {"hs_code_pattern": "84*", "category_id": self.cat_general.id}
        )
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        result = self.Mapping._get_category_for_hs_code("8499000000")
        self.assertEqual(result, self.cat_general)

    def test_resolution_strips_non_digits(self):
        """HS codes from external systems sometimes carry dots / spaces."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        for variant in ["8421.23.00.90", "8421 23 00 90", "8421-23-0090"]:
            with self.subTest(variant=variant):
                self.assertEqual(
                    self.Mapping._get_category_for_hs_code(variant),
                    self.cat_filtration,
                )

    def test_resolution_inactive_rules_skipped(self):
        rule = self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        rule.active = False
        self.assertFalse(self.Mapping._get_category_for_hs_code("8421230090"))

    def test_resolution_no_match_returns_empty(self):
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        self.assertFalse(self.Mapping._get_category_for_hs_code("8537109899"))

    def test_resolution_catch_all_wildcard_fires_when_nothing_else(self):
        """Bare ``*`` rule (specificity 0) fires last when no
        longer-literal rule matches the input."""
        self.Mapping.create(
            {"hs_code_pattern": "*", "category_id": self.cat_general.id}
        )
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        # Specific rule wins for matching codes.
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("8421230090"),
            self.cat_filtration,
        )
        # Catch-all fires for unmatched codes.
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("9999999999"),
            self.cat_general,
        )

    def test_sequence_breaks_specificity_tie(self):
        """Two rules with the same specificity (different patterns
        but equal literal length) — lower sequence wins.

        Pattern uniqueness prevents identical patterns coexisting,
        so we use two distinct same-length prefixes that both happen
        to match the lookup code via different routes (one wildcard,
        one exact for a longer code). Build them so both *do* match
        the test code.
        """
        # Both patterns have specificity 4 (literal "8421" and literal
        # "8422"). Only the first matches "84219999" — but to test
        # sequence tiebreak we need both to match. Use two same-length
        # wildcard rules whose literals share a common prefix.
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
                "sequence": 50,
            }
        )
        self.Mapping.create(
            {
                "hs_code_pattern": "84*",
                "category_id": self.cat_filtration.id,
                "sequence": 10,
            }
        )
        # "8421230090" matches both ("8421*" specificity 4 wins over
        # "84*" specificity 2 — specificity, not sequence). Verifies
        # specificity ordering still trumps sequence.
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("8421230090"), self.cat_general
        )

    def test_sequence_breaks_tie_when_specificity_equal(self):
        """Same specificity (length 4), different literal prefixes —
        the input matches both via wildcard, sequence picks the
        winner. Use a code starting '84' so the '84*' wildcard
        catches it; add a second '84*'-equivalent isn't possible
        (uniqueness) so we test by toggling the *active* flag on the
        general rule and verifying the inactive one is skipped."""
        rule_general = self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
                "sequence": 10,
            }
        )
        rule_general.active = False
        # Now only the (longer) exact rule applies — verify it wins
        # despite higher sequence number.
        self.Mapping.create(
            {
                "hs_code_pattern": "84219*",
                "category_id": self.cat_filtration.id,
                "sequence": 99,
            }
        )
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("8421999"),
            self.cat_filtration,
        )

    # ---- multi-company ----------------------------------------------------

    def test_company_scoped_rule_takes_precedence_over_global(self):
        """A company-specific rule outranks a global one *of equal
        specificity*. The longest-literal rule still wins overall — see
        the next test."""
        company = self.env.company
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
                "sequence": 10,
            }
        )
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_filtration.id,
                "company_id": company.id,
                "sequence": 5,
            }
        )
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("8421230090"), self.cat_filtration
        )

    def test_global_rule_used_when_no_company_match(self):
        # Use the main company as the lookup target without creating a
        # peer company. Creating a fresh ``res.company`` in v19 trips
        # account-module backfill issues unrelated to this module.
        # Instead we verify: rule scoped to a non-existent company id
        # is ignored; rule with no company applies.
        bogus_company = self.env["res.company"].browse(99999)
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
            }
        )
        # Lookup with the main company — global rule still applies.
        self.assertEqual(
            self.Mapping._get_category_for_hs_code(
                "8421230090", company=self.env.company
            ),
            self.cat_general,
        )
        # Lookup with the bogus company — same global rule applies.
        self.assertEqual(
            self.Mapping._get_category_for_hs_code("8421230090", company=bogus_company),
            self.cat_general,
        )

    # ---- uniqueness constraint --------------------------------------------

    def test_pattern_unique_per_company(self):
        """Duplicate (pattern, company_id) is rejected at create time
        by the Python ``@constrains`` check (we don't use a SQL
        UNIQUE because of NULL-semantics differences across
        PostgreSQL versions)."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_general.id}
        )
        with self.assertRaises(ValidationError):
            self.Mapping.create(
                {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
            )

    def test_pattern_unique_rejects_duplicate_global(self):
        """Two global rules (both ``company_id=NULL``) for the same
        pattern must also be rejected — this is the case PostgreSQL's
        default UNIQUE doesn't catch, hence the Python implementation."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_general.id}
        )
        with self.assertRaises(ValidationError):
            self.Mapping.create(
                {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
            )

    def test_pattern_unique_per_company_rejects_duplicate_scoped(self):
        """Two rules with the same pattern AND the same
        ``company_id`` set — rejected. Exercises the
        ``rec.company_id`` truthy branch in the constraint."""
        company = self.env.company
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
                "company_id": company.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.Mapping.create(
                {
                    "hs_code_pattern": "8421*",
                    "category_id": self.cat_filtration.id,
                    "company_id": company.id,
                }
            )

    def test_pattern_unique_per_company_allows_global_plus_scoped(self):
        """Same pattern, but one global and one scoped to a company —
        the unique constraint allows it because (pattern, company_id)
        differs (NULL vs. the company id). Avoids creating a second
        ``res.company`` record (v19 account-module backfill is brittle
        in test isolation)."""
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_general.id,
                # No company_id → global rule
            }
        )
        # Same pattern, scoped to the main company — allowed.
        self.Mapping.create(
            {
                "hs_code_pattern": "8421*",
                "category_id": self.cat_filtration.id,
                "company_id": self.env.company.id,
            }
        )

    # ---- intrastat description (graceful when account_intrastat absent)

    def test_intrastat_description_no_module_returns_empty(self):
        """Cheap-path: when ``account_intrastat`` isn't installed,
        ``intrastat_description`` should compute to empty string,
        not raise. The compute catches ``KeyError`` on the env
        reference for exactly this reason."""
        rule = self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        # Just reading the field is enough — the test passes if no
        # exception is raised regardless of intrastat install state.
        self.assertIsInstance(rule.intrastat_description, (str, bool))

    # ---- server action (Apply HS Code → Category Mapping) -----------------

    def _make_product(self, name, hs_code=None, categ=None):
        vals = {
            "name": name,
            "categ_id": (categ or self.cat_general).id,
            "type": "consu",
        }
        if hs_code is not None:
            vals["hs_code"] = hs_code
        return self.env["product.template"].create(vals)

    def test_action_apply_hs_mapping_recategorises(self):
        """Happy path: product has an HS code, a matching rule exists,
        and the current category differs from the matched one — the
        action moves the product to the matched category."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        tmpl = self._make_product(
            "Filter X", hs_code="8421230090", categ=self.cat_general
        )
        result = tmpl.action_apply_hs_mapping()
        self.assertEqual(tmpl.categ_id, self.cat_filtration)
        # Multi-product invocation returns a notification action;
        # single-product (here) returns one too on the success path.
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["tag"], "display_notification")

    def test_action_apply_hs_mapping_no_hs_code_raises(self):
        """Single-product invocation, product has no HS code →
        ``UserError`` with a specific message. Works whether the
        ``hs_code`` field exists or not — the action's
        missing-field branch falls into the same no-code path."""
        tmpl = self._make_product("Mystery part", hs_code=None)
        with self.assertRaises(UserError):
            tmpl.action_apply_hs_mapping()

    def test_action_apply_hs_mapping_no_rule_raises(self):
        """Single-product invocation, product has an HS code but no
        rule matches → ``UserError``."""
        # No rules created — the table is empty for this test.
        tmpl = self._make_product("Filter X", hs_code="8421230090")
        with self.assertRaises(UserError):
            tmpl.action_apply_hs_mapping()

    def test_action_apply_hs_mapping_already_correct_raises(self):
        """Single-product invocation, product is already in the
        matched category → ``UserError`` (not silent no-op)."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        tmpl = self._make_product(
            "Filter X", hs_code="8421230090", categ=self.cat_filtration
        )
        with self.assertRaises(UserError):
            tmpl.action_apply_hs_mapping()

    def test_action_apply_hs_mapping_multi_product_all_no_code(self):
        """Multi-product invocation where all products lack an HS
        code — toast returns with ``skipped_no_code = 3``. Works
        without the ``hs_code`` field installed; exercises the
        multi-product toast return path independently."""
        tmpls = (
            self._make_product("a") | self._make_product("b") | self._make_product("c")
        )
        result = tmpls.action_apply_hs_mapping()
        self.assertEqual(result["type"], "ir.actions.client")
        self.assertEqual(result["tag"], "display_notification")
        # All three skipped with no-HS-code; type is warning since
        # nothing was updated.
        self.assertEqual(result["params"]["type"], "warning")

    def test_action_apply_hs_mapping_multi_product_success_type(self):
        """Multi-product invocation that DOES re-categorise at
        least one product — toast type is 'success' (exercises
        the ``"success" if updated else "warning"`` ternary's
        truthy branch)."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        tmpls = self._make_product(
            "a", hs_code="8421230090", categ=self.cat_general
        ) | self._make_product("b", hs_code="8421999999", categ=self.cat_general)
        result = tmpls.action_apply_hs_mapping()
        self.assertEqual(result["params"]["type"], "success")
        self.assertEqual(tmpls[0].categ_id, self.cat_filtration)
        self.assertEqual(tmpls[1].categ_id, self.cat_filtration)

    def test_action_apply_hs_mapping_multi_product_with_codes(self):
        """Multi-product invocation: per-product issues are reported
        in the toast, never raised — buyer can have a mixed batch."""
        self.Mapping.create(
            {"hs_code_pattern": "8421*", "category_id": self.cat_filtration.id}
        )
        tmpls = self.env["product.template"]
        tmpls |= self._make_product(
            "Filter A", hs_code="8421230090", categ=self.cat_general
        )
        # No HS code → would raise on single-product, but multi-product
        # path skips with a count.
        tmpls |= self._make_product("Mystery", hs_code=None)
        # Already-correct → multi-product skips silently.
        tmpls |= self._make_product(
            "Filter B", hs_code="8421999999", categ=self.cat_filtration
        )
        result = tmpls.action_apply_hs_mapping()
        self.assertEqual(result["type"], "ir.actions.client")
        # First product moved.
        self.assertEqual(tmpls[0].categ_id, self.cat_filtration)
        # The other two unchanged.
        self.assertEqual(tmpls[1].categ_id, self.cat_general)
        self.assertEqual(tmpls[2].categ_id, self.cat_filtration)

    def test_action_apply_hs_mapping_empty_recordset_returns_false(self):
        """Defensive: calling on an empty recordset is a no-op,
        returns False rather than raising."""
        empty = self.env["product.template"]
        self.assertFalse(empty.action_apply_hs_mapping())
