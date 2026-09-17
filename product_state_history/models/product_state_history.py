# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductStateHistory(models.Model):
    _name = "product.state.history"
    _description = "Product State History"
    _order = "date desc, id desc"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
        index=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Changed by",
        default=lambda self: self.env.user,
        required=True,
        ondelete="restrict",
    )
    old_state_id = fields.Many2one(
        comodel_name="product.state",
        string="Previous State",
        ondelete="restrict",
    )
    new_state_id = fields.Many2one(
        comodel_name="product.state",
        required=True,
        ondelete="restrict",
    )
    reason = fields.Text(required=True)

    @api.depends("old_state_id", "new_state_id")
    def _compute_display_name(self):
        for rec in self:
            old = rec.old_state_id.display_name or self.env._("None")
            new = rec.new_state_id.display_name or self.env._("None")
            rec.display_name = f"{old} \u2192 {new}"
