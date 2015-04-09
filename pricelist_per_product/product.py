# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Sylvain CALADOR
#    Copyright 2015 Akretion
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

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def default_pricelist_item_ids(self):
        """ You may inherit it """
        versions = self.env['product.pricelist.version'].search(
            [('pricelist_id.price_grid', '=', True)])
        res = []
        for vers in versions:
            res.append({
                'price_version_id': vers.id,
                'price_discount': -1,
                'sequence': 1,
                'base': 1,
            })
        return res

    def _default_pricelist_item_ids(self):
        return self.default_pricelist_item_ids()

    pricelist_item_ids = fields.One2many(
        'product.pricelist.item',
        'product_tmpl_id',
        # domain=[('price_version_id.pricelist_id.type', '=', 'sale'),
        #         ('price_version_id.price_grid', '=', True)],
        string='Pricelist Items',
        default=_default_pricelist_item_ids,
        help="These prices are defined with absolute values\n"
             "(no calculation with discount)"
    )
