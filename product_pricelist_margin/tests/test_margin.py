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
        cls.env.ref("product.group_sale_pricelist").users |= cls.env.user

    def test_margin_computation_compute_price(self):
        self.assertEqual(self.line.cost, 20.0)
        self.assertEqual(self.line.margin, (35 - 20))
        self.assertEqual(self.line.margin_percent, ((35 - 20) / 35) * 100)
