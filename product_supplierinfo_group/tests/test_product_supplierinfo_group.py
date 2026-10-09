# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from copy import deepcopy

import lxml.etree as etree

from odoo import Command
from odoo.tests import common


class Test(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_sofa = cls.env.ref("product.consu_delivery_01_product_template")
        cls.vendor_gemini = cls.env.ref("base.res_partner_3")

    @property
    def supplierinfo_vals(self):
        return {
            "partner_id": self.vendor_gemini.id,
            "product_tmpl_id": self.product_sofa.id,
            "product_name": "aProductName",
            "product_code": "aProductCode",
            "min_qty": 5.0,
            "price": 10.0,
            "delay": 1,
        }.copy()

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
        # minimal case
        self.assertIn(pretty_html(group.unit_price_note), PATTERN1)
        # more complex case
        min_50 = deepcopy(self.supplierinfo_vals)
        min_50.update({"min_qty": 50.0, "price": 8.0})
        min_500 = deepcopy(self.supplierinfo_vals)
        min_500.update({"min_qty": 500.0, "price": 6.0})
        self.env["product.supplierinfo"].create([min_500, min_50])
        self.assertIn(pretty_html(group.unit_price_note), PATTERN2)

    def test_delete_supplierinfo_line_from_variant_form(self):
        """A supplierinfo line deleted from a group via the variant form must
        be removed exactly once.

        If no fix, the unlink command is played twice because
        supplierinfo_group_ids is a non-stored related field: the first run
        already unlinks the supplierinfo line in database, then the framework
        re-plays the whole write once the related cache is invalidated.

        For a non-superuser, the second unlink raises MissingError (the
        access check evaluates the company rule on the record that no longer
        exists).
        """
        variant = self.product_sofa.product_variant_id
        group = self.env["product.supplierinfo.group"].create(
            {
                "product_tmpl_id": self.product_sofa.id,
                "partner_id": self.vendor_gemini.id,
            }
        )
        lines = self.env["product.supplierinfo"].create(
            [
                dict(self.supplierinfo_vals, group_id=group.id),
                dict(self.supplierinfo_vals, group_id=group.id, min_qty=50.0),
            ]
        )
        # with_user() drops superuser mode (su=False), so the replayed unlink may raise
        # MissingError if no fix.
        variant.with_user(self.env.ref("base.user_admin")).write(
            {
                "supplierinfo_group_ids": [
                    Command.update(
                        group.id, {"supplierinfo_ids": [Command.delete(lines[0].id)]}
                    )
                ]
            }
        )
        self.assertEqual(group.supplierinfo_ids.ids, [lines[1].id])


def pretty_html(html_markup):
    return etree.tostring(
        etree.fromstring(html_markup.__str__()),
        method="html",
        pretty_print=True,
        encoding=str,
    )


PATTERN1 = """
<div class="table_price_note">
  <div class="table_price_note_row">
    <span class="table_price_note_cell">5.0</span>
    <span class="table_price_note_cell">10.0 Units</span>
  </div>
</div>\n"""


PATTERN2 = """
<div class="table_price_note">
  <div class="table_price_note_row">
    <span class="table_price_note_cell">5.0</span>
    <span class="table_price_note_cell">10.0 Units</span>
  </div>
  <div class="table_price_note_row">
    <span class="table_price_note_cell">50.0</span>
    <span class="table_price_note_cell">8.0 Units</span>
  </div>
  <div class="table_price_note_row">
    <span class="table_price_note_cell">500.0</span>
    <span class="table_price_note_cell">6.0 Units</span>
  </div>
</div>\n"""
