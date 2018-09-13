# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.tests import common


class TestProductSupplierinfoRevision(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductSupplierinfoRevision, cls).setUpClass()
        cls.vendor = cls.env['res.partner'].create({
            'name': 'Suplier test',
            'supplier': True,
        })
        cls.today = datetime.today()
        cls.supplierinfo = cls.env['product.supplierinfo'].create({
            'name': cls.vendor.id,
            'price': 100.0,
        })

    def test_product_supplierinfo_revision(self):
        # run wizard
        wizard = self.env['product.supplierinfo.duplicate.wizard'].create({
            'date_start': self.today + relativedelta(days=1),
            'variation_percent': 25.0,
        })
        result = wizard.with_context(
            active_ids=self.supplierinfo.ids).action_apply()
        self.assertEqual(result['name'], 'Supplier Pricelist')
        new_supplierinfo = self.env['product.supplierinfo'].browse(
            result['domain'][0][2][0]
        )
        self.assertEqual(
            self.supplierinfo.date_end,
            self.today.strftime('%Y-%m-%d'),
        )
        self.assertEqual(
            new_supplierinfo.date_start,
            (self.today + relativedelta(days=1)).strftime('%Y-%m-%d')
        )
        self.assertAlmostEqual(new_supplierinfo.price, 125.0)
