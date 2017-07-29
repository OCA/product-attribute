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

            template_id = vals.get('product_tmpl_id')
            try:
                value_ids = vals.get('attribute_value_ids')[0][2]
            except IndexError:
                return super(ProductProduct, self).create(vals)

            exclusion_values = exclusion_obj.search(
                ['|',
                 ('product_tmpl_ids', 'in', [template_id]),
                 ('product_tmpl_ids', 'in', []),
                 ('attribute_value_ids', 'in', value_ids),
                 ])

            for excl in exclusion_values:
                if set(excl.attribute_value_ids.ids) <= set(value_ids):
                    return self
        return super(ProductProduct, self).create(vals)
