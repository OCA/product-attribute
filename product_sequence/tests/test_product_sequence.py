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
from psycopg2 import IntegrityError


class ProductSequenceCase(TransactionCase):

    def setUp(self):
        super(ProductSequenceCase, self).setUp()

    def test_copy(self):
        original = self.env.ref('product.product_product_1')
        new = original.copy()
        self.assertFalse(original.default_code == new.default_code)

    def test_create(self):
        product_obj = self.env['product.product']
        new = product_obj.create({'name': 'Test'})
        self.assertTrue(new.default_code)

    def test_write_slash(self):
        product = self.env.ref('product.product_product_1')
        self.cr.execute("""
            UPDATE product_product
              SET default_code = '/'
              WHERE id=%s""", (product.id,))
        product.write({'name': 'Test'})
        self.assertFalse(product.default_code == '/')

    def test_write_false(self):
        product = self.env.ref('product.product_product_1')
        with self.assertRaises(IntegrityError):
            product.default_code = False
