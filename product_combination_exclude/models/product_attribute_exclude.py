# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeExclude(models.Model):

    _name = 'product.attribute.exclude'
    _description = 'Product Attribute Exclude'
    _rec_name = 'attribute_value_ids'

    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Incompatible Attributes',
    )

    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        string='Product Templates',
    )

    matrix_id = fields.Many2one(
        comodel_name='product.attribute.exclude.matrix',
        string='Exclusion Matrix',
    )
