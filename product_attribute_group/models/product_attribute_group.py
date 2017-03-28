# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductAttributeGroup(models.Model):

    _name = 'product.attribute.group'
    _description = 'Product Attribute Group'

    name = fields.Char()
    attribute_line_ids = fields.One2many(
        comodel_name='product.attribute.group.line',
        inverse_name='product_attr_group_id',
        string='Product Attributes')


class ProductAttributeGroupLine(models.Model):

    _name = 'product.attribute.group.line'
    _description = 'Product Attribute Group Line'

    product_attr_group_id = fields.Many2one(
        comodel_name='product.attribute.group',
        string='Product Template',
        ondelete='cascade',
        required=True)
    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Attribute',
        ondelete='restrict',
        required=True)
    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Attribute Values')

    @api.constrains('value_ids', 'attribute_id')
    def _check_valid_attribute(self):
        if any(line.value_ids > line.attribute_id.value_ids for line in self):
            raise ValidationError(
                _('Error ! You cannot use this attribute '
                  'with the following value.'))
        return True
