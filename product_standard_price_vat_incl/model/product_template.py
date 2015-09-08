# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Standard Price VAT Included Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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


from openerp.osv import fields
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp


class product_template(Model):
    _inherit = 'product.template'

    def _get_template_from_product(self, cr, uid, ids, context=None):
        """Find the products to trigger when a Tax changes"""
        product_obj = self.pool['product.product']
        products = product_obj.browse(cr, uid, ids, context=context)
        res = [x.product_tmpl_id.id for x in products]
        return res

    def _get_standard_price_vat_incl(
            self, cr, uid, ids, name, arg, context=None):
        res = {}
        at_obj = self.pool['account.tax']
        for pt in self.browse(cr, uid, ids, context=context):
            taxes = at_obj.compute_all(
                cr, uid, pt.taxes_id, pt.standard_price, 1,
                force_excluded=True)
            res[pt.id] = taxes['total_included']
        return res

    _columns = {
        'standard_price_vat_incl': fields.function(
            _get_standard_price_vat_incl, string='Cost VAT Included',
            type='float', digits_compute=dp.get_precision('Product Price'),
            help="""Cost price of the product based on:\n"""
            """* Cost;\n"""
            """* Customer Taxes;\n"""
            """This cost will be Cost x Taxes and works only if you have"""
            """ set Taxes with VAT include in the price""",
            method=True, store={
                'product.product': (
                    _get_template_from_product, [
                        'standard_price',
                        'taxes_id',
                    ], 10),
                'product.template': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'standard_price',
                        'taxes_id',
                    ], 10),
            }),
    }
