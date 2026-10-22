# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestMargin(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "default_code": "pricelist-margin-product",
                "name": "Demo Margin Product",
                "list_price": 40.0,
                "standard_price": 20.0,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "pricelist",
            }
        )

        cls.line = cls.env["product.pricelist.item"].create(
            {
                "pricelist_id": cls.pricelist.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "compute_price": "fixed",
                "applied_on": "1_product",
                "fixed_price": 35,
                "min_quantity": 1,
            }
        )

    def test_margin_with_fixed_price_computation(self):
        self.assertEqual(self.line.cost, 20.0)
        self.assertEqual(self.line.margin, (35 - 20))
        self.assertEqual(self.line.margin_percent, 42.86)

        # Copy production and test that margin is computed based on current item
        # => self.line should not impact margin of new_line
        new_line = self.line.copy()
        new_line.fixed_price = 40
        self.assertEqual(new_line.margin, (40 - 20))
        self.assertEqual(new_line.margin_percent, 50.00)

    def test_margin_with_discount_computation(self):
        self.line.write({"compute_price": "percentage", "percent_price": 0.5})
        self.assertAlmostEqual(self.line.margin_percent, 49.75)

    def test_margin_global_applied_on(self):
        # Coverage for applied_on not in ("1_product", "0_product_variant")
        global_line = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "compute_price": "fixed",
                "applied_on": "3_global",
                "fixed_price": 35,
            }
        )
        self.assertEqual(global_line.margin, 0)
        self.assertEqual(global_line.margin_percent, 0)

    def test_margin_zero_price(self):
        # Coverage for float_is_zero(price)
        zero_line = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "compute_price": "fixed",
                "applied_on": "1_product",
                "fixed_price": 0,
            }
        )
        self.assertEqual(zero_line.margin, 0)
        self.assertEqual(zero_line.margin_percent, 0)
