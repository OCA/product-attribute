#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    products_price_pricelist_id = fields.Many2one(
        related="company_id.products_price_pricelist_id",
        readonly=False,
    )
