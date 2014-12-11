# -*- coding: utf-8 -*-
##############################################################################
#
#    Author Vincent Renaville. Copyright 2013 Camptocamp SA
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
from openerp.osv import orm


class product_product(orm.Model):
    _inherit = "product.product"

    def _supplier_not_company(self, cr, uid, ids, context=None):
        company_pool = self.pool['res.company']
        # Get all company
        all_company_ids = company_pool.search(cr, uid, [], context=context)
        all_partner_company = company_pool.read(cr, uid,
                                                all_company_ids,
                                                ['partner_id'],
                                                context=context)
        company_partner_ids = [x['partner_id'][0] for x in all_partner_company]
        # Get all partner attached to partner
        current_product = self.browse(cr, uid, ids, context=context)[0]
        product_supplier_ids = [x.name.id for x in current_product.seller_ids]
        intersection_partner = set(company_partner_ids).intersection(
            product_supplier_ids)
        if intersection_partner:
            # some supplier refer to our company so refuse it
            return False
        else:
            return True

    _constraints = [
        (_supplier_not_company, """You cannot defined
         your company has a product supplier""",
         ['seller_ids']),
        ]
