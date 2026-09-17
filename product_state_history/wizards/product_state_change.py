# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.exceptions import UserError


class ProductStateChangeWizard(models.TransientModel):
    _name = "product.state.change.wizard"
    _description = "Change Product State"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    old_state_id = fields.Many2one(
        related="product_tmpl_id.product_state_id",
        string="Current State",
        readonly=True,
    )
    new_state_id = fields.Many2one(
        comodel_name="product.state",
        required=True,
        domain="[('id', '!=', old_state_id)]",
    )
    reason = fields.Text(required=True)

    def action_apply(self):
        self.ensure_one()
        reason = (self.reason or "").strip()
        if not reason:
            raise UserError(
                self.env._("Please provide a reason for this state change.")
            )
        if self.new_state_id == self.old_state_id:
            raise UserError(self.env._("Please select a different state."))
        self.product_tmpl_id._change_product_state(self.new_state_id, reason)
        return {"type": "ir.actions.act_window_close"}
