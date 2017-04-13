# -*- coding: utf-8 -*-
# Copyright 2014- Odoo Community Association - OCA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

from .helper_methods import render_default_code


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.onchange('name')
    def onchange_name(self):
        if self.name and not self.code:
            self.code = self.name[0:2]

    code = fields.Char(
        string='Code', default=onchange_name)
    comment = fields.Text('Comment')

    @api.model
    def create(self, values):
        if 'code' not in values:
            values['code'] = values.get('name', '')[0:2]
        value = super(ProductAttributeValue, self).create(values)
        return value

    @api.multi
    def write(self, vals):
        result = super(ProductAttributeValue, self).write(vals)
        if 'code' in vals:
            attribute_line_obj = self.env['product.attribute.line']
            product_obj = self.env['product.product']
            for attr_value in self:
                cond = [('attribute_id', '=', attr_value.attribute_id.id)]
                attribute_lines = attribute_line_obj.search(cond)
                for line in attribute_lines:
                    cond = [('product_tmpl_id', '=', line.product_tmpl_id.id),
                            ('manual_code', '=', False)]
                    products = product_obj.with_context(
                        active_test=False).search(cond)
                    for product in products:
                        if product.reference_mask:
                            render_default_code(product,
                                                product.reference_mask)
        return result
