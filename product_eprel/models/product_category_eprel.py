# Copyright 2025 Juan Carlos Oñate - Tecnativa <juancarlos.onate@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategoryEprel(models.Model):
    _name = "product.category.eprel"
    _description = "EPREL Product Category"

    name = fields.Char(string="Product group", required=True)
    code = fields.Char(string="Code", required=True)
