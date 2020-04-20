# -*- coding: utf-8 -*-
# Copyright 2019 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_categ_ids = fields.Many2many(
        comodel_name='product.category', relation='product_list_categ_rel',
        column1='product_id', column2='categ_id', string='Lists')
