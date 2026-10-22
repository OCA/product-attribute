# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2018 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductSupplierinfoRevision(BaseCommon):
    _test_user_groups = ("product.group_product_manager",)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Suplier test"})
        cls.today = fields.Date.today()
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "standard_price": 50.0,
            }
        )
        cls.supplierinfo = cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.vendor.id,
                "price": 100.0,
                "product_tmpl_id": cls.product_template.id,
            }
        )

    def test_product_supplierinfo_revision(self):
        # run wizard
        wizard = self.env["product.supplierinfo.duplicate.wizard"].create(
            {
                "date_start": self.today + relativedelta(days=1),
                "variation_percent": 25.0,
            }
        )
        result = wizard.with_context(active_ids=self.supplierinfo.ids).action_apply()
        self.assertEqual(result["res_model"], "product.supplierinfo")
        new_supplierinfo = self.env["product.supplierinfo"].browse(
            result["domain"][0][2][0]
        )
        self.assertEqual(
            self.supplierinfo.date_end.strftime("%Y-%m-%d"),
            self.today.strftime("%Y-%m-%d"),
        )
        self.assertEqual(
            new_supplierinfo.date_start.strftime("%Y-%m-%d"),
            (self.today + relativedelta(days=1)).strftime("%Y-%m-%d"),
        )
        self.assertAlmostEqual(new_supplierinfo.price, 125.0)
        self.assertEqual(new_supplierinfo.previous_info_id, self.supplierinfo)
        self.assertAlmostEqual(new_supplierinfo.previous_price, 100.0)
        self.assertAlmostEqual(new_supplierinfo.variation_percent, 25.0)
        self.assertAlmostEqual(self.supplierinfo.variation_percent, 0.0)

    def test_future_revision_visible_in_action(self):
        wizard = self.env["product.supplierinfo.duplicate.wizard"].create(
            {"date_start": self.today + relativedelta(days=10)}
        )
        result = wizard.with_context(active_ids=self.supplierinfo.ids).action_apply()
        self.assertNotIn("search_default_active", result["context"])

    def test_revision_with_inconsistent_dates(self):
        self.supplierinfo.date_start = self.today + relativedelta(days=5)
        wizard = self.env["product.supplierinfo.duplicate.wizard"].create(
            {"date_start": self.today + relativedelta(days=1)}
        )
        with self.assertRaises(ValidationError):
            wizard.with_context(active_ids=self.supplierinfo.ids).action_apply()
