# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import Form, TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env.ref("base.user_root").write(
            {"groups_id": [(4, self.env.ref("uom.group_uom").id)]}
        )
        self.unit_kg = self.env.ref("uom.product_uom_kgm")
        self.unit_litre = self.env.ref("uom.product_uom_litre")

    def test_domain(self):
        product_form = Form(self.env["product.template"])
        product_form.name = "Demo Product"
        product_form.uom_id = self.unit_kg
        product_form.uom_po_id = self.unit_litre
        self.assertEqual(product_form.uom_po_id, self.unit_kg)

        product_form.uom_id = self.unit_litre
        product_form.uom_po_id = self.unit_litre
        self.assertEqual(product_form.uom_po_id, self.unit_litre)
