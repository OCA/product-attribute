# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    state = fields.Selection(
        track_visibility="onchange",
        inverse="_inverse_state_history",
    )

    @api.multi
    def _prepare_product_state_history_values(self):
        self.ensure_one()
        vals = {
            "product_template_id": self.id,
            "product_state": self.state,
        }
        return vals

    @api.multi
    def _inverse_state_history(self):
        history_obj = self.env["product.state.history"]
        for template in self:
            history_obj.create(template._prepare_product_state_history_values())

    @api.multi
    def action_product_state_history(self):
        action = self.env.ref("product_state_history.product_state_history_act_window")
        result = action.read()[0]
        result.update({"domain": [("product_template_id", "in", self.ids)]})

        return result
