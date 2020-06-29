# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def open_filter_application_wizard(self):
        self.ensure_one()
        action = {
            'name': _('Select Products by Applications'),
            'type': 'ir.actions.act_window',
            'res_model': 'filter.application.wizard',
            'target': 'new',
            'view_mode': 'form',
            'context': {'from_sale_order': True},
        }

        return action
