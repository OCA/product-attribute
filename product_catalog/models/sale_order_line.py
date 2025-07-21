# Copyright 2025 Kencove (http://www.kencove.com).
# @author Mohamed Alkobrosli <malkobrosly@kencove.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def action_add_from_catalog(self):
        order = self.env["sale.order"].browse(self.env.context.get("order_id"))
        return order.with_context(child_field="order_line").custom_add_from_catalog()
