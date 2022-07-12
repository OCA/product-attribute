# Copyright (C) 2021-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class Productproduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def button_margin_per_pricelist(self):
        self.ensure_one()
        view = self.env.ref(
            "product_pricelist_margin.view_wizard_preview_pricelist_margin_form"
        )
        return {
            'name': _('See Margins per Pricelist'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.preview.pricelist.margin',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {},
        }
