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
from openerp.tools.misc import mute_logger
from psycopg2 import IntegrityError


class ProductSequenceCase(TransactionCase):

    def setUp(self):
        super(ProductSequenceCase, self).setUp()
        self.product_obj = self.env['product.product'].with_context(
            recompute=False)
        self.product = self.env.ref('product.product_product_1').with_context(
            recompute=False)

    def test_copy(self):
        new = self.product.copy()
        self.assertFalse(self.product.default_code == new.default_code)

    def test_create(self):
        new = self.product_obj.create({'name': 'Test'})
        self.assertTrue(new.default_code)

    def test_write_slash(self):
        self.cr.execute("""
            UPDATE product_product
              SET default_code = '/'
              WHERE id=%s""", (self.product.id,))
        self.product.write({'name': 'Test'})
        self.assertFalse(self.product.default_code == '/')

    @mute_logger('openerp.sql_db')
    def test_write_false(self):
        with self.assertRaises(IntegrityError):
            self.product.default_code = False
