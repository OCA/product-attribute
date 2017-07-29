# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductAttributeExclude(models.Model):

    _name = 'product.attribute.exclude'
    _description = 'Product Attribute Exclude'
    _rec_name = 'attribute_value_ids'

    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Incompatible Attributes',
        required=True,
    )
    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        string='Product Templates',
    )
    matrix_id = fields.Many2one(
        comodel_name='product.attribute.exclude.matrix',
        string='Exclusion Matrix',
    )

    @api.constrains('attribute_value_ids')
    def _check_values_attributes_uniqueness(self):
        if (len(self.attribute_value_ids.ids) !=
                len(self.attribute_value_ids.mapped('attribute_id'))):
            raise ValidationError(
                _('You cannot have multiple values from the '
                  'same attribute in an exclusion.'))
