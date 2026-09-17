# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import AccessError
from odoo.orm.domains import Domain


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_state_id = fields.Many2one(tracking=False)
    product_state_history_ids = fields.One2many(
        comodel_name="product.state.history",
        inverse_name="product_tmpl_id",
        string="State History",
        copy=False,
    )
    product_state_history_count = fields.Integer(
        string="State History Count",
        compute="_compute_product_state_history_count",
    )

    @api.depends("product_state_history_ids")
    def _compute_product_state_history_count(self):
        grouped = dict(
            self.env["product.state.history"]._read_group(
                domain=Domain("product_tmpl_id", "in", self.ids),
                groupby=["product_tmpl_id"],
                aggregates=["__count"],
            )
        )
        for template in self:
            template.product_state_history_count = grouped.get(template, 0)

    def write(self, vals):
        if "product_state_id" in vals:
            new_state_id = vals.get("product_state_id") or False
            changing = self.filtered(lambda t: t.product_state_id.id != new_state_id)
            if changing:
                reason = (
                    self.env.context.get("product_state_change_reason") or ""
                ).strip()
                changing._check_product_state_change_access()
                changing._create_product_state_history(new_state_id, reason)
        return super().write(vals)

    def _check_product_state_change_access(self):
        if self.env.su:
            return
        if not self.env.user.has_group(
            "product_state_history.group_product_state_change"
        ):
            raise AccessError(
                self.env._("You are not allowed to change the product state.")
            )

    def _create_product_state_history(self, new_state_id, reason):
        self.env["product.state.history"].create(
            [
                {
                    "product_tmpl_id": template.id,
                    "old_state_id": template.product_state_id.id,
                    "new_state_id": new_state_id,
                    "reason": reason,
                    "user_id": self.env.user.id,
                    "date": fields.Datetime.now(),
                }
                for template in self
            ]
        )

    def _change_product_state(self, new_state, reason):
        """Change the product state and record the reason in the history."""
        self.with_context(product_state_change_reason=reason).write(
            {"product_state_id": new_state.id}
        )

    def action_change_product_state(self):
        self.ensure_one()
        self._check_product_state_change_access()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Change Product State"),
            "res_model": "product.state.change.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_product_tmpl_id": self.id,
            },
        }

    def action_open_product_state_history(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product_state_history.action_product_state_history"
        )
        action["domain"] = [("product_tmpl_id", "=", self.id)]
        action["context"] = {
            "default_product_tmpl_id": self.id,
            "search_default_product_tmpl_id": self.id,
        }
        return action
