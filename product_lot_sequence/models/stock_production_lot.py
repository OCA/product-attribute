# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id and self.product_id.product_tmpl_id.lot_sequence_id:
            self.name = self.product_id.product_tmpl_id.lot_sequence_id._next()
