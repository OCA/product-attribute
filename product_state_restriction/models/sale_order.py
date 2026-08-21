# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        self._check_product_state_restriction()
        return super().action_confirm()

    def _check_product_state_restriction(self):
        for order in self:
            for line in order.order_line:
                if not line.product_id:
                    continue
                state = line.product_id.product_tmpl_id.product_state_id
                if state and state.restrict_sale:
                    raise UserError(_(
                        "Product '%(product)s' is in state '%(state)s' and cannot be sold.",
                        product=line.product_id.display_name,
                        state=state.name,
                    ))