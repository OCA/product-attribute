# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductAttributeValue(models.Model):

    _inherit = 'product.attribute.value'

    name = fields.Char()
    product_attr_group_id = fields.Many2many(
        comodel_name='product.attribute.group',
        string='Attribute Group'
        )
