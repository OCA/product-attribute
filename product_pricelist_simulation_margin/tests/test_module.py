# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# Copyright (C) 2023 - Hugo Córdoba FactorLibre (http://www.factorlibre.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestModule(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "C02 Tax",
                "amount": "0.00",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "default_code": "pricelist-margin-product",
                "name": "Demo Product (Margin per Pricelist module)",
                "list_price": 40.0,
                "standard_price": 20.0,
                "taxes_id": cls.tax,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "pricelist",
                "discount_policy": "without_discount",
            }
        )
        cls.wizard = (
            cls.env["wizard.preview.pricelist"]
            .with_context(active_model="product.product", active_id=cls.product.id)
            .create({})
        )

    def test_margin_computation(self):
        line = self.wizard._prepare_simulation_lines_vals(self.product, self.pricelist)
        self.assertEqual(line.get("margin"), 20.0)
        self.assertEqual(line.get("margin_percent"), 50.0)
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "compute_price": "fixed",
                "applied_on": "1_product",
                "fixed_price": 35,
            }
        )
        line = self.wizard._prepare_simulation_lines_vals(self.product, self.pricelist)
        self.assertEqual(line.get("margin"), 15.0)
        self.assertEqual(line.get("margin_percent"), 42.857142857142854)
