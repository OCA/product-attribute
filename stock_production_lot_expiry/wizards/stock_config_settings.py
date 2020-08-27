# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockConfigSettings(models.TransientModel):

    _inherit = 'stock.config.settings'

    production_lot_expiry_date_field = fields.Selection(
        selection="_selection_production_lot_expiry_date_field",
        string="Lot/serial date field name used as expiration date",
    )

    @api.model
    def _selection_production_lot_expiry_date_field(self):
        return self.env["stock.production.lot"]._selection_expiry_date_field()

    @api.model
    def get_default_production_lot_expiry_date_field(self, fields):
        icp = self.env["ir.config_parameter"]
        return {
            "production_lot_expiry_date_field": icp.get_param(
                "stock_production_lot_expiry.field_name", "life_date"
            )
        }

    @api.multi
    def set_production_lot_expiry_date_field(self):
        self.env["ir.config_parameter"].set_param(
            "stock_production_lot_expiry.field_name",
            self.production_lot_expiry_date_field,
        )

    @api.model
    def get_production_lot_expiry_date_field(self):
        icp = self.env["ir.config_parameter"]
        return icp.get_param(
            "stock_production_lot_expiry.field_name", "life_date"
        )
