# Copyright 2022-2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form, new_test_user
from odoo.tests.common import users

from odoo.addons.base.tests.common import BaseCommon


class TestProductSupplierinfoStockPickingType(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier"})
        cls.picking_in_a = cls.env["stock.picking.type"].create(
            {
                "name": "Incoming A",
                "code": "incoming",
                "sequence_code": "IN-A",
                "warehouse_id": cls.warehouse.id,
            }
        )
        cls.picking_in_b = cls.env["stock.picking.type"].create(
            {
                "name": "Incoming B",
                "code": "incoming",
                "sequence_code": "IN-B",
                "warehouse_id": cls.warehouse.id,
            }
        )
        cls.picking_in_c = cls.env["stock.picking.type"].create(
            {
                "name": "Incoming C",
                "code": "incoming",
                "sequence_code": "IN-C",
                "warehouse_id": cls.warehouse.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "is_storable": True,
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.supplier.id,
                            "min_qty": 1,
                            "price": 5,
                            "picking_type_id": cls.picking_in_a.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.supplier.id,
                            "min_qty": 1,
                            "price": 10,
                            "picking_type_id": cls.picking_in_b.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "partner_id": cls.supplier.id,
                            "min_qty": 1,
                            "price": 20,
                        },
                    ),
                ],
            }
        )
        new_test_user(
            cls.env,
            login="test_purchase_user",
            groups="purchase.group_purchase_user,stock.group_stock_multi_locations",
        )

    def _create_purchase_order(self, picking_type_id):
        order_form = Form(self.env["purchase.order"])
        order_form.partner_id = self.supplier
        order_form.picking_type_id = picking_type_id
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return order_form.save()

    @users("test_purchase_user")
    def test_product_picking_type_a(self):
        po = self._create_purchase_order(self.picking_in_a)
        self.assertEqual(po.order_line.price_unit, 5)

    @users("test_purchase_user")
    def test_product_picking_type_b(self):
        po = self._create_purchase_order(self.picking_in_b)
        self.assertEqual(po.order_line.price_unit, 10)

    @users("test_purchase_user")
    def test_product_picking_type_c(self):
        po = self._create_purchase_order(self.picking_in_c)
        self.assertEqual(po.order_line.price_unit, 20)
        po.picking_type_id = self.picking_in_a
        po.onchange_picking_type_id()
        self.assertEqual(po.order_line.price_unit, 5)
