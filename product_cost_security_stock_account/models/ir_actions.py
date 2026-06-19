# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import AccessError

_COST_PROTECTED_ACTIONS = frozenset(
    {
        "stock_account.action_report_stock_valuation",
        "stock_account.stock_avco_report_action",
        "stock_account.stock_move_valuation_action",
    }
)


class IrActionsActions(models.Model):
    _inherit = "ir.actions.actions"

    @api.model
    def _for_xml_id(self, full_xml_id):
        action = super()._for_xml_id(full_xml_id)
        if full_xml_id in _COST_PROTECTED_ACTIONS:
            if not self.env.user.has_group(
                "product_cost_security.group_product_cost"
            ):
                raise AccessError(
                    _("You are not allowed to access inventory valuation reports.")
                )
        return action
