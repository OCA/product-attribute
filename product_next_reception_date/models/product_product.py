# Copyright 2024 Akretion (http://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    next_reception_date = fields.Date(
        compute="_compute_next_reception_date", compute_sudo=True
    )

    def _compute_next_reception_date(self):
        moves = self.env["stock.move"].search(self._get_next_reception_domain())
        move_dict = {
            move.product_id: move.picking_id.scheduled_date
            for move in sorted(
                moves, key=lambda m: m.picking_id.scheduled_date, reverse=True
            )
        }
        for record in self:
            record.next_reception_date = move_dict.get(record)

    def _get_next_reception_domain(self):
        """In case of several warehouses by company,
        you may choose to refine these conditions"""
        return [
            ("picking_id.state", "in", ["confirmed", "waiting", "assigned"]),
            ("picking_type_id.code", "=", "incoming"),
            ("company_id", "=", self.env.company.id),
            ("product_id", "in", self.ids),
        ]
