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
        moves = self.env["stock.move"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("product_id", "in", self.ids),
                ("picking_type_id.code", "=", "incoming"),
                (
                    "state",
                    "in",
                    ["waiting", "confirmed", "partially_available", "assigned"],
                ),
            ],
            order="date desc",
        )
        # because of order by desc the last move by product is the earlier
        move_dict = {move.product_id: move.date for move in moves}
        for record in self:
            record.next_reception_date = move_dict.get(record)
