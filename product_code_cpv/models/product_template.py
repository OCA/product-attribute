# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_template_cpv_id = fields.Many2one(
        'product.template.cpv',
        string='CPV Code',
        help='Common Procurement Vocabulary Code',
    )
