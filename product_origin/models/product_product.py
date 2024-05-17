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

    state_id_domain = fields.Binary(
        compute="_compute_state_id_domain",
        help="Technical field, used to compute dynamically state domain"
        " depending on the country.",
    )

    @api.constrains("country_id", "state_id")
    def _check_country_id_state_id(self):
        for product in self.filtered(lambda x: x.state_id and x.country_id):
            if product.country_id != product.state_id.country_id:
                raise ValidationError(
                    _(
                        "The state '%(state_name)s' doesn't belong to"
                        " the country '%(country_name)s'",
                        state_name=product.state_id.name,
                        country_name=product.country_id.name,
                    )
                )

    @api.onchange("country_id")
    def onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False

    @api.onchange("state_id")
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id

    @api.depends("country_id")
    def _compute_state_id_domain(self):
        for product in self.filtered(lambda x: x.country_id):
            product.state_id_domain = [("country_id", "=", product.country_id.id)]
        for product in self.filtered(lambda x: not x.country_id):
            product.state_id_domain = []
