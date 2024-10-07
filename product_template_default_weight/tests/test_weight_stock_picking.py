# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestWeightStockPicking(TransactionCase):
    def setUp(self):
        super().setUp()
        self.warehouse = self.env.ref("stock.warehouse0")
        self.product_temp_id = self.env.ref(
            "product.product_product_11_product_template"
        )
        self.product_id1 = self.env.ref("product.product_product_11")
        self.product_id1.write(
            {
                "weight": 0,
            }
        )
        self.product_id2 = self.env.ref("product.product_product_11b")
        self.product_id2.write(
            {
                "weight": 100,
            }
        )

        self.partner_id = self.env.ref("base.res_partner_12")

    def test_weight_purchase_order_picking(self):
        self.product_temp_id.write(
            {
                "weight": 50,
            }
        )
        self.purchase_order_id = self.env["purchase.order"].create(
            {
                "partner_id": self.partner_id.id,
                "date_planned": datetime.today(),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id1.id,
                            "product_qty": 2,
                            "price_unit": 10,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id2.id,
                            "product_qty": 2,
                            "price_unit": 10,
                        },
                    ),
                ],
            }
        )

        self.purchase_order_id.button_confirm()
        picking_id = self.purchase_order_id.picking_ids
        self.assertEqual(picking_id.weight, 300)

    def test_weight_sale_order_picking(self):
        self.product_temp_id.write(
            {
                "weight": 50,
            }
        )
        self.env["stock.quant"].create(
            [
                {
                    "product_id": self.product_id1.id,
                    "location_id": self.warehouse.lot_stock_id.id,
                    "quantity": 2,
                },
                {
                    "product_id": self.product_id2.id,
                    "location_id": self.warehouse.lot_stock_id.id,
                    "quantity": 2,
                },
            ]
        )
        self.sale_order_id = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id1.id,
                            "product_uom_qty": 2,
                            "price_unit": 10,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id2.id,
                            "product_uom_qty": 2,
                            "price_unit": 10,
                        },
                    ),
                ],
            }
        )

        self.sale_order_id.action_confirm()
        picking_id = self.sale_order_id.picking_ids
        self.assertEqual(picking_id.weight, 300)

    def test_weight_template_from_variant(self):
        product_id = self.env.ref("product.product_product_4_product_template")
        product_id.weight = 10
        self.assertEqual(product_id.weight, 10)
        product_variant_id = self.env.ref("product.product_product_4")
        product_variant_id.write({"weight": 20})
        self.assertEqual(product_id.weight, 10)
