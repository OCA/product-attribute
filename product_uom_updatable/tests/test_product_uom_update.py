# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import SavepointCase


class TestProductUomUpdate(SavepointCase):
    def setUp(self):
        super(TestProductUomUpdate, self).setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))
        self.uom_unit = self.env.ref("uom.product_uom_unit")
        self.uom_day = self.env.ref("uom.product_uom_day")
        self.product = self.env.ref("product.product_delivery_01")
        self.product_tmpl_id = self.env.ref(
            "product.product_delivery_01_product_template"
        )
        self.partner_id = self.ref("base.res_partner_4")
        self.picking_type_id = self.ref("stock.picking_type_in")
        self.location_id = self.ref("stock.stock_location_suppliers")
        self.location_dest_id = self.ref("stock.stock_location_stock")

    def test_update_uom(self):
        self.picking_in = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_id,
                "partner_id": self.partner_id,
                "location_id": self.location_id,
                "location_dest_id": self.location_dest_id,
            }
        )

        self.env["stock.move"].create(
            {
                "name": self.product.name,
                "product_id": self.product.id,
                "product_uom_qty": 2,
                "product_uom": self.product.uom_id.id,
                "picking_id": self.picking_in.id,
                "location_id": self.location_id,
                "location_dest_id": self.location_dest_id,
            }
        )
        self.new_uom = self.env["uom.uom"].create(
            {
                "name": "new unit",
                "category_id": self.uom_unit.category_id.id,
                "uom_type": "smaller",
            }
        )

        self.new_uom_other_category = self.env["uom.uom"].create(
            {
                "name": "new unit 2",
                "category_id": self.uom_day.category_id.id,
                "uom_type": "smaller",
            }
        )
        # verify that the product has stock_moves
        self.assertTrue(self.product.stock_move_ids)
        self.assertEqual(self.product.uom_id, self.uom_unit)
        self.assertEqual(self.uom_unit.category_id, self.new_uom.category_id)
        self.assertEqual(
            self.uom_day.category_id, self.new_uom_other_category.category_id
        )
        self.assertEqual(self.uom_unit.factor_inv, self.new_uom.factor_inv)
        self.assertEqual(
            self.uom_day.factor_inv, self.new_uom_other_category.factor_inv
        )
        # uom is changed with another uom with the same category
        self.product_tmpl_id.update({"uom_id": self.new_uom.id})
        self.assertEqual(self.product_tmpl_id.uom_id, self.new_uom)
        # uom_po can also be changed with another uom with the same category
        self.assertEqual(self.product_tmpl_id.uom_po_id, self.uom_unit)
        self.product_tmpl_id.update({"uom_po_id": self.new_uom.id})
        self.assertEqual(self.product_tmpl_id.uom_po_id, self.new_uom)
        # uom is changed with another uom from different category
        with self.assertRaises(UserError):
            self.product_tmpl_id.update({"uom_id": self.new_uom_other_category.id})
        # uom_po is changed with another uom from different category
        with self.assertRaises(UserError):
            self.product_tmpl_id.update({"uom_po_id": self.new_uom_other_category.id})
