# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    image = fields.Binary(string='Image', attachment=True)
