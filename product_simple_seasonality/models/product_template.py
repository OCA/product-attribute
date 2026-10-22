# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seasonality_ids = fields.Many2many(
        "seasonality",
        string="Seasonality",
        help="This is an informative field to "
        "track which seasons this product should be associated with",
    )
