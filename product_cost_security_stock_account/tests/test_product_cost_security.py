from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductCostSecurityStockAccount(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env,
            "stock_cost_user",
            groups="stock.group_stock_manager,base.group_allow_export",
        )
        cls.cost_group = cls.env.ref("product_cost_security.group_product_cost")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Cost security product",
                "is_storable": True,
                "standard_price": 12.0,
                "categ_id": cls.env["product.category"]
                .create(
                    {
                        "name": "Standard cost category",
                        "property_cost_method": "standard",
                    }
                )
                .id,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.env.ref("stock.stock_location_stock"), 5.0
        )

    def test_cost_access_and_group_changes(self):
        product = self.product.with_user(self.user)
        fields = ["standard_price", "avg_cost", "total_value"]
        expected = {"standard_price": 12.0, "avg_cost": 12.0, "total_value": 60.0}
        for allowed in (False, True, False, True):
            self.user.group_ids = [
                Command.link(self.cost_group.id)
                if allowed
                else Command.unlink(self.cost_group.id)
            ]
            with self.subTest(allowed=allowed):
                metadata = product.fields_get(fields)
                if allowed:
                    self.assertEqual(set(metadata), set(fields))
                    self.assertEqual(
                        product.read(fields)[0], dict(expected, id=product.id)
                    )
                    self.assertEqual(
                        product.export_data(fields)["datas"], [[12.0, 12.0, 60.0]]
                    )
                else:
                    self.assertFalse(metadata)
                    self.assertEqual(
                        product.read(["name"])[0]["name"], self.product.name
                    )
                    for field in fields:
                        with self.subTest(field=field):
                            with self.assertRaises(AccessError):
                                product.read([field])
                            with self.assertRaises(AccessError):
                                product.export_data([field])
        self.assertEqual(self.product.read(fields)[0], dict(expected, id=product.id))
