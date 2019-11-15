# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.template_obj = self.env["product.template"]
        self.both_unit = self.env.ref("uom.product_uom_litre")
        self.sale_unit = self.env.ref("product_uom_use_type.product_uom_pint")
        self.product_template = self.env.ref(
            "product_uom_use_type.product_bier_faucheuse"
        )

    # Test Section
    def test_01_onchange_template(self):

        self.product_template.uom_id = self.both_unit
        self.product_template._onchange_uom_id()
        self.assertEqual(
            self.product_template.uom_po_id.use_type,
            self.both_unit.use_type,
            "Setting a 'both' unit as main UoM should set the same as Purchase"
            " UoM",
        )

        # Change unit to sale unit
        # Should NOT change po_uom_id to the same
        uom_po_id_before = self.product_template.uom_po_id
        self.product_template.uom_id = self.sale_unit
        self.product_template._onchange_uom_id()
        self.assertEqual(
            self.product_template.uom_po_id,
            uom_po_id_before,
            "Setting a 'sale' unit as main UoM should not change the purchase"
            " UoM",
        )
