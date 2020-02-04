# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        select_type = self.env.context.get("select_type", False)
        if select_type:
            res.update(
                {
                    "customer": select_type == "customer",
                    "supplier": select_type == "supplier",
                }
            )
        return res
