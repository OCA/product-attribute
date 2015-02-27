# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: David BEAL
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

from openerp import (
    models,
    fields,
    api,
    _,
)

PRICE_GRID_HELP = _("""Define if the price list items are filled
from product form with a grid of specific values
for each product""")

ACTION = {
    'res_model': 'product.template',
    'type': 'ir.actions.act_window',
    'target': 'current',
}

HELP_NAME_ON_ACTION = _("Filter and Select products and click on "
                        "'More' button and 'Set Price Items'")


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    price_grid = fields.Boolean(
        string='Product Price Grid',
        help=PRICE_GRID_HELP)


class ProductPricelistVersion(models.Model):
    _inherit = 'product.pricelist.version'

    @api.depends('product_in_version_count')
    def count_products(self):
        # TODO: security rule multicompany
        query_in = """SELECT product_tmpl_id
        FROM product_pricelist_item
        WHERE price_version_id = %s """
        for record in self:
            self.env.cr.execute(query_in, [self.id])
            products_in_nbr = len(set(self.env.cr.fetchall()))
            self.product_in_version_count = products_in_nbr
            self.product_out_version_count = (len(self.env['product.template'].
                                              search([])) - products_in_nbr)

    price_grid = fields.Boolean(
        related='pricelist_id.price_grid',
        domain=[('price_surcharge', '=', 0)],
        #readonly=True,
        store=True,
        help=PRICE_GRID_HELP)
    product_in_version_count = fields.Integer(
        string="Products with this Version",
        compute='count_products')
    product_out_version_count = fields.Integer(
        string="Products without this Version",
        compute='count_products')
    item_grid_ids = fields.One2many(
        'product.pricelist.item',
        'price_version_id')

    @api.multi
    def goto_products_in_version(self):
        context = self.env.context.copy()
        context['price_version_id'] = self.id
        action = {
            'domain': [
                ('pricelist_item_ids.price_version_id', '=', self.id)],
            'name': HELP_NAME_ON_ACTION,
            'view_mode': 'tree',
            'view_id': self.env.ref(
                'pricelist_per_product.product_template_tree_price_view').id,
            'context': context,
        }
        action.update(ACTION)
        print context, '     context'
        return action

    @api.multi
    def goto_products_outside_version(self):
        #fix it
        action = {
            'domain': [
                '|',
                ('pricelist_item_ids', '=', False),
                ('pricelist_item_ids.price_version_id', '!=', self.id)],
            'name': HELP_NAME_ON_ACTION,
            'view_mode': 'tree',
            'view_id': self.env.ref(
                'pricelist_per_product.product_template_tree_price_view').id,
            'context': {'price_version_id': self.id},
        }
        action.update(ACTION)
        return action


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    date_end = fields.Date(
        related='price_version_id.date_end',
        readonly=True)
    currency_name = fields.Many2one(
        related='price_version_id.pricelist_id.currency_id',
        readonly=True)

    @api.multi
    def goto_product_template(self):
        action = {
            'name': 'Product',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
        }
        action.update(ACTION)
        return action
