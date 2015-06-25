# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP / Odoo, Open Source Management Solution - module extension
#    Copyright (C) 2014- O4SB (<http://openforsmallbusiness.co.nz>).
#    Author Graeme Gellatly <g@o4sb.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests.common import TransactionCase
from openerp import pooler


class CustomerProductPricingCase(TransactionCase):

    def setUp(self):
        super(CustomerProductPricingCase, self).setUp()
        self.pool = pooler.get_pool(self.cr.dbname)

    def test_name_get(self):
        list_id = self.env.ref('product.list0').id
        try:
            self.pool['product.pricelist'].name_get(
                self.cr, self.uid, list_id)
        except Exception:
            self.fail("Pricelist name_get failed")

    def test_view_partner_pricing(self):
        partner_obj = self.pool['res.partner']
        partner_id = [self.env.ref('base.res_partner_1').id]
        result = partner_obj.view_partner_pricing(
            self.cr, self.uid, partner_id)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['type'] == 'ir.actions.act_window')
