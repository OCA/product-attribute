#  Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import tagged

from .common import TestPricelistItemUomCommon


@tagged("post_install", "-at_install")
class TestProductPricelistItemUom(TestPricelistItemUomCommon):
    def test_allowed_uom_ids(self):
        rule = self._create_rule(fixed_price=10.0)
        self.assertEqual(rule.allowed_uom_ids, self.uom_unit | self.uom_pack_6)

    def test_pricelist_packaging_rules(self):
        """The rule matching the requested packaging is the one selected."""
        # Unscoped rule, created first so that it is last in ``_order``.
        self._create_rule(fixed_price=30.0, min_quantity=6)
        rule_unit = self._create_rule(
            fixed_price=10.0, min_quantity=6, uom_id=self.uom_unit.id
        )
        rule_pack = self._create_rule(
            fixed_price=20.0, min_quantity=6, uom_id=self.uom_pack_6.id
        )

        self.assertEqual(
            self.pricelist._get_product_rule(self.product_tmpl, 6.0, uom=self.uom_unit),
            rule_unit.id,
        )
        self.assertEqual(
            self.pricelist._get_product_rule(
                self.product_tmpl, 6.0, uom=self.uom_pack_6
            ),
            rule_pack.id,
        )

    def test_rule_without_uom_stays_unrestricted(self):
        """A rule without packaging keeps applying whatever the requested UoM."""
        rule = self._create_rule(fixed_price=10.0, min_quantity=6)

        self.assertEqual(
            self.pricelist._get_product_rule(self.product_tmpl, 6.0, uom=self.uom_unit),
            rule.id,
        )
        self.assertEqual(
            self.pricelist._get_product_rule(
                self.product_tmpl, 1.0, uom=self.uom_pack_6
            ),
            rule.id,
        )
        self.assertFalse(
            self.pricelist._get_product_rule(self.product_tmpl, 5.0, uom=self.uom_unit)
        )

    def test_min_quantity_expressed_in_rule_uom(self):
        """``min_quantity`` is compared in the packaging of the rule."""
        rule = self._create_rule(
            fixed_price=10.0, min_quantity=5, uom_id=self.uom_pack_6.id
        )

        self.assertEqual(
            self.pricelist._get_product_rule(
                self.product_tmpl, 5.0, uom=self.uom_pack_6
            ),
            rule.id,
        )
        self.assertFalse(
            self.pricelist._get_product_rule(
                self.product_tmpl, 4.0, uom=self.uom_pack_6
            )
        )

    def test_uom_cleared_on_category_rule_creation(self):
        rule = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": self.product_category.id,
                "compute_price": "fixed",
                "fixed_price": 10.0,
                "uom_id": self.uom_pack_6.id,
            }
        )
        self.assertFalse(rule.uom_id)

    def test_uom_cleared_on_category_rule_write(self):
        rule = self._create_rule(fixed_price=10.0, uom_id=self.uom_pack_6.id)
        self.assertEqual(rule.uom_id, self.uom_pack_6)

        rule.write(
            {
                "applied_on": "2_product_category",
                "categ_id": self.product_category.id,
            }
        )
        self.assertFalse(rule.uom_id)
