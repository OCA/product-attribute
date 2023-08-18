# Copyright 2016 Tecnativa - Sergio Teruel
# Copyright 2018 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestProductSupplierinfoRevision(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Suplier test"})
        cls.today = datetime.today()
        cls.supplierinfo = cls.env["product.supplierinfo"].create(
            {"partner_id": cls.vendor.id, "price": 100.0}
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
