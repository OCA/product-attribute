# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    production_lot_expiry_date_field = fields.Selection(
        selection="_selection_production_lot_expiry_date_field",
        string="Lot/serial date field name used as expiration date",
        config_parameter="stock_production_lot_expiry.field_name",
    )

    @api.model
    def _selection_production_lot_expiry_date_field(self):
        return self.env["stock.lot"]._selection_expiry_date_field()

    @api.model
    def get_default_production_lot_expiry_date_field(self, fields):
        icp = self.env["ir.config_parameter"]
        return {
            "production_lot_expiry_date_field": icp.get_param(
                "stock_production_lot_expiry.field_name", "expiration_date"
            )
        }

    @api.model
    def get_production_lot_expiry_date_field(self):
        icp = self.env["ir.config_parameter"]
        return icp.get_param(
            "stock_production_lot_expiry.field_name", "expiration_date"
        )
