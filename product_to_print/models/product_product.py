# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    category_print_id = fields.Many2one(
        string='Print Category', related='product_tmpl_id.category_print_id')

    to_print = fields.Boolean(string='To Print')

    @api.model
    def create(self, vals):
        if vals.get('category_print_id', False):
            vals['to_print'] = True
        return super(ProductProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        product_ids = []
        for product in self:
            if product.category_print_id:
                if len(list(
                        set(vals.keys()) &
                        set(product.category_print_id.field_ids.
                            mapped('name')))):
                    product_ids.append(product.id)
        products = self.browse(product_ids)
        super(ProductProduct, products).write({'to_print': True})
        return res
