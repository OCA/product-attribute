# -*- coding: utf-8 -*-
# Copyright 2019 bitwise.solutions <https://bitwise.solutions>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplateCPV(models.Model):
    _name = 'product.template.cpv'

    name = fields.Char()
    code = fields.Integer()
    description = fields.Char()
