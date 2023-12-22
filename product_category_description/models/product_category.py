# Copyright 2022 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    description = fields.Char(string="Description", default="", copy=False)
