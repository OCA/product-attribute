# Copyright 2020 Acsone SA/NV
# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductUomUpdate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_day = cls.env.ref("uom.product_uom_day")
        cls.product_tmpl_id = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "uom_id": cls.uom_unit.id,
            }
        )
        cls.product = cls.product_tmpl_id.product_variant_id
        cls.partner_id = cls.env["res.partner"].create({"name": "Test Partner"})
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
                "relative_uom_id": cls.uom_unit.id,
                "relative_factor": 1.0,
            }
        )

        cls.new_uom_other_category = cls.env["uom.uom"].create(
            {
                "name": "new unit 2",
                "relative_uom_id": cls.uom_day.id,
                "relative_factor": 1.0,
            }
        )

    def test_update_uom(self):
        # verify that the product has stock_moves
        self.assertTrue(self.product.stock_move_ids)
        self.assertEqual(self.product.uom_id, self.uom_unit)
        self.assertTrue(self.uom_unit._has_common_reference(self.new_uom))
        self.assertTrue(self.uom_day._has_common_reference(self.new_uom_other_category))
        self.assertEqual(self.uom_unit.factor, self.new_uom.factor)
        self.assertEqual(self.uom_day.factor, self.new_uom_other_category.factor)
        # uom is changed with another uom with the same category
        self.product_tmpl_id.update({"uom_id": self.new_uom.id})
        self.assertEqual(self.product_tmpl_id.uom_id, self.new_uom)
        # uom is changed with another uom from different category
        with self.assertRaises(UserError):
            self.product_tmpl_id.update({"uom_id": self.new_uom_other_category.id})
