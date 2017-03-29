# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductAttributeGroup(models.Model):

    _name = 'product.attribute.group'
    _description = 'Product Attribute Group'

    name = fields.Char()
    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Product Attribute',
        ondelete='restrict',
        required=True)
    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Product Attribute Values')
    attribute_line_ids = fields.Many2many(
        comodel_name='product.attribute.line',
        string='Product Attributes')

    @api.multi
    def update_products(self):
        self.ensure_one()
        for tmpl in self.product_tmpl_ids:
            attr_line = tmpl.attribute_line_ids.filtered(
                lambda al: al.attribute_id == self.attribute_id)
            attr_line.value_ids |= self.value_ids
            tmpl.write({})
