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
    'type': 'ir.actions.act_window',
    'target': 'current',
}

HELP_NAME_ON_ACTION = _("Change all your '%s' prices in one time "
                        "by click on 'More' button")


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
        compute='count_products',
        help="Number of Product Template with this Pricelist version")
    product_out_version_count = fields.Integer(
        string="Product Template without this Version",
        compute='count_products',
        help="Number of Product Template without this Pricelist version")
    item_grid_ids = fields.One2many(
        'product.pricelist.item',
        'price_version_id')

    @api.multi
    def button_product_in_version(self):
        return self.with_context(
            price_version_id=self.id).goto_products_from_version('product.product', 'in')

    @api.multi
    def button_template_in_version(self):
        return self.goto_products_from_version('product.template', 'in')

    @api.multi
    def button_product_out_version(self):
        return self.goto_products_from_version('product.product', 'out')

    @api.multi
    def button_template_out_version(self):
        return self.with_context(
            price_version_id=self.id).goto_products_from_version('product.template', 'out')
            # 'context': self.env[model].with_context(price_version_id=self.id)

    @api.model
    def goto_products_from_version(self, model, direction):
        print '     ctx', self.env.context
        if model == 'product.product':
            view_name = 'product'
        else:
            view_name = 'product_template'
        if direction == 'in':
            domain = [('pricelist_item_ids.price_version_id', '=', self.id)]
        else:
            domain = [('= ', '=', 'done')]
        action_name = view_name.replace('_', ' ') + 's'
        view_id_ref = 'pricelist_per_product.%s_tree_price_view' % view_name
        ctx = self.env.context.copy()
        ctx['price_version_id'] = self.id
        action = {
            'domain': domain,
            'name': HELP_NAME_ON_ACTION % action_name,
            'view_mode': 'tree',
            'res_model': model,
            'view_id': self.env.ref(view_id_ref).id,
            'context': ctx
        }
        action.update(ACTION)
        print '     action', action
        return action


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    date_end = fields.Date(
        related='price_version_id.date_end',
        readonly=True)
    currency_name = fields.Many2one(
        related='price_version_id.pricelist_id.currency_id',
        readonly=True)
    related_sequence = fields.Integer(
        String='Sequence',
        related="sequence")

    @api.multi
    def button_product_product(self):
        return self.goto_product('product.product')

    @api.multi
    def button_product_template(self):
        return self.goto_product('product.template')

    @api.model
    def goto_product(self, model):
        if model == 'product.product':
            product = self.product_id.id
        else:
            product = self.product_tmpl_id.id
        action = {
            'name': 'Product',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': product,
            'res_model': model,
        }
        action.update(ACTION)
        return action
