# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestWeightStockPicking(TransactionCase):
    def setUp(self):
        super().setUp()
        self.warehouse = self.env.ref("stock.warehouse0")
        self.product_tmpl = self.env.ref("product.product_product_11_product_template")
        self.product_no_weight = self.env.ref("product.product_product_11")
        self.product_no_weight.write({"weight": 0})
        self.product_with_weight = self.env.ref("product.product_product_11b")
        self.product_with_weight.write({"weight": 100})
        self.partner = self.env.ref("base.res_partner_12")
        self.stock_location = self.warehouse.lot_stock_id
        self.customer_location = self.env.ref("stock.stock_location_customers")
        self.supplier_location = self.env.ref("stock.stock_location_suppliers")

    def _create_picking(self, location, location_dest, products):
        picking = self.env["stock.picking"].create(
            {
                "partner_id": self.partner.id,
                "picking_type_id": self.warehouse.out_type_id.id,
                "location_id": location.id,
                "location_dest_id": location_dest.id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "name": product["product"].name,
                            "product_id": product["product"].id,
                            "product_uom_qty": product["qty"],
                            "product_uom": product["product"].uom_id.id,
                            "location_id": location.id,
                            "location_dest_id": location_dest.id,
                        },
                    )
                    for product in products
                ],
            }
        )
        return picking

    def test_weight_variant_zero_uses_template(self):
        self.product_tmpl.write({"weight": 50})
        picking = self._create_picking(
            self.supplier_location,
            self.stock_location,
            [
                {"product": self.product_no_weight, "qty": 2},
                {"product": self.product_with_weight, "qty": 2},
            ],
        )
        self.assertEqual(picking.weight, 300)

    def test_weight_variant_defined_ignores_template(self):
        self.product_tmpl.write({"weight": 50})
        picking = self._create_picking(
            self.supplier_location,
            self.stock_location,
            [{"product": self.product_with_weight, "qty": 2}],
        )
        self.assertEqual(picking.weight, 200)

    def test_weight_both_zero(self):
        self.product_tmpl.write({"weight": 0})
        picking = self._create_picking(
            self.supplier_location,
            self.stock_location,
            [{"product": self.product_no_weight, "qty": 2}],
        )
        self.assertEqual(picking.weight, 0)

    def test_weight_template_not_overridden_by_variant(self):
        self.product_tmpl.weight = 10
        single_variant = self.env.ref("product.product_product_4")
        single_variant.write({"weight": 20})
        self.assertEqual(self.product_tmpl.weight, 10)

    def test_shipping_weight_wizard_uses_template(self):
        self.product_tmpl.write({"weight": 50})
        picking = self._create_picking(
            self.stock_location,
            self.customer_location,
            [{"product": self.product_no_weight, "qty": 2}],
        )
        picking.action_confirm()
        picking.action_assign()
        for ml in picking.move_line_ids:
            ml.qty_done = ml.reserved_uom_qty
        wizard = self.env["choose.delivery.package"].create(
            {
                "picking_id": picking.id,
            }
        )
        wizard._compute_shipping_weight()
        self.assertEqual(wizard.shipping_weight, 100)
