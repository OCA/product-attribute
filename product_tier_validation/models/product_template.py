# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "tier.validation"]
    _tier_validation_manual_config = False

    @property
    @tools.ormcache()
    def _state_to(self):
        return (
            self.env["product.state"]
            .search([])
            .filtered(
                lambda x, s=self: x.code not in (s._state_from + [s._cancel_state])
            )
            .mapped("code")
        )

    def write(self, vals):
        # Tier Validation does not work with Stages, only States :-(
        # So, signal state transition by adding it to the vals
        if "product_state_id" in vals:
            stage_id = vals.get("product_state_id")
            stage = self.env["product.state"].browse(stage_id)
            vals["state"] = stage.code  # yes, "code" is used to represent a "state"
        res = super().write(vals)
        if "product_state_id" in vals:
            self.restart_validation()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        states = self.env["product.state"].search([("code", "in", self._state_from)])
        if not states:
            raise UserError("Wrong configuration of '_state_from' in product.state")
        for vals in vals_list:
            if vals.get("product_state_id") not in states.ids:
                vals["product_state_id"] = states[0].id
        return super().create(vals_list)
