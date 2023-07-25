# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country of Origin",
        ondelete="restrict",
    )

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Country State of Origin",
        ondelete="restrict",
    )

    @api.constrains("country_id", "state_id")
    def _chekc_country_id_state_id(self):
        for product in self.filtered(lambda x: x.state_id and x.country_id):
            if product.country_id != product.state_id.country_id:
                raise ValidationError(
                    _(
                        f"The state '{product.state_id.name}' doesn't belong to"
                        f" the country '{product.country_id.name}'"
                    )
                )

    @api.onchange("country_id")
    def onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
