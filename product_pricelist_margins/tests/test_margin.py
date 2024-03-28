# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, TransactionCase


class TestMargin(TransactionCase):
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
            }
        )
        cls.env.ref("product.group_sale_pricelist").users |= cls.env.user

    def test_margin_computation_compute_price(self):
        self.assertEqual(self.line.cost, 20.0)
        self.assertEqual(self.line.margin, (35 - 20))
        self.assertEqual(self.line.margin_percent, ((35 - 20) / 35) * 100)

    def test_margin_computation_percentage(self):
        with Form(self.line) as line:
            line.compute_price = "percentage"
            self.assertEqual(line.cost, 20.0)
            self.assertEqual(line.margin, 0)
            self.assertEqual(line.margin_percent, 0)

    def test_margin_computation_formula(self):
        with Form(self.line) as line:
            line.compute_price = "formula"
            self.assertEqual(line.cost, 20.0)
            self.assertEqual(line.margin, 0)
            self.assertEqual(line.margin_percent, 0)
