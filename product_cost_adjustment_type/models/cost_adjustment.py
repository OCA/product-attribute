# Copyright 2021 - Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class CostAdjustment(models.Model):
    _inherit = "cost.adjustment"

    type_id = fields.Many2one(
        "cost.adjustment.type",
        string="Type",
        required=True,
        states={"draft": [("readonly", False)]},
    )
    account_id = fields.Many2one(
        "account.account",
        string="Account",
        related="type_id.account_id",
    )

    def action_post(self):
        # res = super().action_post()
        if not self.exists():
            return
        self.ensure_one()
        if not self.user_has_groups("stock.group_stock_manager"):
            raise UserError(_("Only a stock manager can post a cost adjustment."))
        if self.state != "done":
            raise UserError(
                _(
                    "You can't post the cost adjustment '%s', maybe this cost adjustment "
                    "has been already posted or isn't ready.",
                    self.name,
                )
            )
        self._check_negative()
        for line in self.line_ids:
            line.product_id._change_price(line.product_cost, self.type_id.account_id)
        self.write({"state": "posted", "date": fields.Datetime.now()})
