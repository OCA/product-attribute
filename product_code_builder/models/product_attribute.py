# coding: utf-8
# © 2015 Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from .helper_methods import render_default_code


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    code = fields.Char('Code')

    @api.multi
    def write(self, vals):
        result = super(ProductAttribute, self).write(vals)
        if 'code' in vals:
            attribute_line_obj = self.env['product.attribute.line']
            product_obj = self.env['product.product']
            for attribute in self:
                cond = [('attribute_id', '=', attribute.id)]
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
