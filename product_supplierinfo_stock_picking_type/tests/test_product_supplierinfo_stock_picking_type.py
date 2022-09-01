# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form, common


class TestProductSupplierinfoStockPickingType(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.buy_route = cls.env.ref("purchase_stock.route_warehouse0_buy")
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
                "type": "product",
                "seller_ids": [
                    (
                        0,
                        0,
                        {
                            "name": cls.supplier.id,
                            "min_qty": 1,
                            "price": 5,
                            "picking_type_id": cls.picking_in_a.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.supplier.id,
                            "min_qty": 1,
                            "price": 10,
                            "picking_type_id": cls.picking_in_b.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": cls.supplier.id,
                            "min_qty": 1,
                            "price": 20,
                        },
                    ),
                ],
            }
        )

    def _create_purchase_order(self, picking_type_id):
        order_form = Form(self.env["purchase.order"])
        order_form.partner_id = self.supplier
        order_form.picking_type_id = picking_type_id
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return order_form.save()

    def test_product_picking_type_a(self):
        po = self._create_purchase_order(self.picking_in_a)
        self.assertEqual(po.order_line.price_unit, 5)

    def test_product_picking_type_b(self):
        po = self._create_purchase_order(self.picking_in_b)
        self.assertEqual(po.order_line.price_unit, 10)

    def test_product_picking_type_c(self):
        po = self._create_purchase_order(self.picking_in_c)
        self.assertEqual(po.order_line.price_unit, 20)
        po.picking_type_id = self.picking_in_a
        po.onchange_picking_type_id()
        self.assertEqual(po.order_line.price_unit, 5)
