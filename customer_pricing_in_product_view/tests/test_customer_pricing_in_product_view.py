# -*- coding: utf-8 -*-
# © 2014 O4SB <http://o4sb.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class CustomerProductPricingCase(TransactionCase):

    def test_name_get(self):
        product_pricelist = self.env.ref('product.list0')
        try:
            product_pricelist.name_get()
        except Exception:
            self.fail("Pricelist name_get failed")

    def test_view_partner_pricing(self):
        partner = self.env.ref('base.res_partner_1')
        result = partner.view_partner_pricing()
        self.assertIsInstance(result, dict)
        self.assertTrue(result['type'] == 'ir.actions.act_window')
