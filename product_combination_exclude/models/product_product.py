# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def create(self, vals):
        vals = {} if vals is None else vals
        if 'attribute_value_ids' in vals:
            exclusion_obj = self.env['product.attribute.exclude']
            search_args = []
            if 'product_tmpl_id' in vals:
                search_args.extend([
                    '|',
                    ('product_tmpl_ids', 'in', [vals['product_tmpl_id']]),
                    ('product_tmpl_ids', 'in', [])])
            try:
                search_args.extend([
                    ('attribute_value_ids', 'in',
                     vals['attribute_value_ids'][0][2])
                ])
            except IndexError:
                return super(ProductProduct, self).create(vals)
            attr_vals = self.env['product.attribute.value'].browse(
                vals['attribute_value_ids'][0][2])
            exclusion_values = exclusion_obj.search(search_args)

            for excl_val in exclusion_values:
                if excl_val.attribute_value_ids <= attr_vals:
                    return self.env['product.product']
            return super(ProductProduct, self).create(vals)
