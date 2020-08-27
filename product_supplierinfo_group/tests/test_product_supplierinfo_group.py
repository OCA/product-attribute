# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from copy import deepcopy


class TestProductSupplierinfoGroup(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_sofa = cls.env.ref("product.consu_delivery_01_product_template")
        cls.vendor_gemini = cls.env.ref("base.res_partner_3")
        cls.supplierinfo_vals = {
            "name": cls.vendor_gemini.id,
            "product_tmpl_id": cls.product_sofa.id,
            "product_name": "aProductName",
            "product_code": "aProductCode",
            "min_qty": 5.0,
            "price": 10.0,
            "delay": 1,
        }

    def test_no_group(self):
        """
        If we try to create a supplierinfo and there is no group yet,
        create a group
        """
        group_before = self.env["product.supplierinfo.group"].search([])
        self.env["product.supplierinfo"].create(self.supplierinfo_vals)
        group = self.env["product.supplierinfo.group"].search(
            [("id", "not in", group_before.ids)]
        )
        self.assertTrue(group)

    def test_has_group(self):
        """
        If we try to create a supplierinfo and there is already a group,
        just add a new line to that group
        """
        group_before = self.env["product.supplierinfo.group"].search([])
        self.env["product.supplierinfo"].create(
            [self.supplierinfo_vals, self.supplierinfo_vals]
        )
        group = self.env["product.supplierinfo.group"].search(
            [("id", "not in", group_before.ids)]
        )
        self.assertEqual(len(group.ids), 1)
        self.assertEqual(len(group.supplierinfo_ids.ids), 2)

    def test_price_note(self):
        """
        Test our price note (Char field display to inform user) is correct
        """
        group_before = self.env["product.supplierinfo.group"].search([])
        self.env["product.supplierinfo"].create([self.supplierinfo_vals])
        group = self.env["product.supplierinfo.group"].search(
            [("id", "not in", group_before.ids)]
        )
        self.assertIn(
            '<td class="table_price_note_cell">5.0</td>', group.unit_price_note,
        )
        self.assertIn(
            '<td class="table_price_note_cell">10.0</td>', group.unit_price_note,
        )
        min_50 = deepcopy(self.supplierinfo_vals)
        min_50.update({"min_qty": 50.0, "price": 8.0})
        min_500 = deepcopy(self.supplierinfo_vals)
        min_500.update({"min_qty": 500.0, "price": 6.0})
        self.env["product.supplierinfo"].create([min_500, min_50])
        self.assertIn(
            '<td class="table_price_note_cell">50.0</td>', group.unit_price_note,
        )
        self.assertIn(
            '<td class="table_price_note_cell">8.0</td>', group.unit_price_note,
        )
        self.assertIn(
            '<td class="table_price_note_cell">500.0</td>', group.unit_price_note,
        )
        self.assertIn(
            '<td class="table_price_note_cell">6.0</td>', group.unit_price_note,
        )
