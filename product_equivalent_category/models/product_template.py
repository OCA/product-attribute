# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    equivalent_categ_id = fields.Many2one(
        "product.equivalent.category",
        "Product Equivalent Category",
        help="Select equivalent category for the current product",
    )
