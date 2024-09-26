# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResConfig(models.TransientModel):
    _inherit = "res.config.settings"

    production_lot_base_date = fields.Selection(
        selection="_selection_production_lot_base_date",
        string="Base date to compute expiration dates",
        config_parameter="stock_production_lot_expired_date.production_lot_base_date",
    )

    @api.model
    def _selection_production_lot_base_date(self):
        return [
            ("use", _("Use date")),
            ("expiration", _("Expiration date")),
            ("alert", _("Alert date")),
            ("removal", _("Removal date")),
        ]
