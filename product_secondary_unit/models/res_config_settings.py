# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    secondary_uom_price_display_sale = fields.Selection(
        related="company_id.secondary_uom_price_display_sale",
        readonly=False,
    )
    secondary_uom_price_display_purchase = fields.Selection(
        related="company_id.secondary_uom_price_display_purchase",
        readonly=False,
    )
    hide_secondary_uom_column_sale = fields.Boolean(
        related="company_id.hide_secondary_uom_column_sale",
        readonly=False,
    )
    hide_secondary_uom_column_purchase = fields.Boolean(
        related="company_id.hide_secondary_uom_column_purchase",
        readonly=False,
    )
