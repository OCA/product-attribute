# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestProductUomUpdate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_day = cls.env.ref("uom.product_uom_day")
        cls.product = cls.env.ref("product.product_delivery_01")
        cls.product_tmpl_id = cls.env.ref(
            "product.product_delivery_01_product_template"
        )
        cls.partner_id = cls.env.ref("base.res_partner_4")
        cls.picking_type_id = cls.env.ref("stock.picking_type_in")
        cls.location_id = cls.env.ref("stock.stock_location_suppliers")
        cls.location_dest_id = cls.env.ref("stock.stock_location_stock")
        cls.picking_in = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.picking_type_id.id,
                "partner_id": cls.partner_id.id,
                "location_id": cls.location_id.id,
                "location_dest_id": cls.location_dest_id.id,
            }
        )

        cls.env["stock.move"].create(
            {
                "name": cls.product.name,
                "product_id": cls.product.id,
                "product_uom_qty": 2,
                "product_uom": cls.product.uom_id.id,
                "picking_id": cls.picking_in.id,
                "location_id": cls.location_id.id,
                "location_dest_id": cls.location_dest_id.id,
            }
        )
        cls.new_uom = cls.env["uom.uom"].create(
            {
                "name": "new unit",
                "category_id": cls.uom_unit.category_id.id,
                "uom_type": "smaller",
            }
        )

        cls.new_uom_other_category = cls.env["uom.uom"].create(
            {
                "name": "new unit 2",
                "category_id": cls.uom_day.category_id.id,
                "uom_type": "smaller",
            }
        )

    def test_update_uom(self):
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
