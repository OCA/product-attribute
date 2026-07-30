# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = [_name, "image.mixin"]

    image = fields.Binary(string="Category Image", attachment=True)
