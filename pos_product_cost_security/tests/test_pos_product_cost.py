# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged, users

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon, TestPoSCommon


@tagged("post_install", "-at_install")
class TestPosProductCostSecurity(TestPointOfSaleCommon, TestPoSCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = cls.basic_config
        cls.product = cls.env.ref("product.product_product_3")

    def _read_product(self, context_values, fields=None):
        """Read product with given context and fields"""
        if fields is None:
            fields = ["name", "standard_price"]
        return (
            self.env["product.product"]
            .with_context(**context_values)
            .browse(self.product.id)
            .read(fields)
        )

    @users("demo")
    def test_pos_session_open_and_override_loader_params(self):
        product_data = self._read_product({"pos_override_cost_security": True})
        self.assertIn("standard_price", product_data[0])

    @users("demo")
    def test_read_with_override_context(self):
        """User with override should see standard_price"""
        product_data = self._read_product({"pos_override_cost_security": True})

        self.assertIn("name", product_data[0])
        self.assertIn(
            "standard_price",
            product_data[0],
            "Standard price should be visible with override",
        )
        self.assertEqual(
            product_data[0]["standard_price"],
            self.env["product.product"].browse(self.product.id).sudo().standard_price,
            "Standard price should match the product cost",
        )
