# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockLot(models.Model):

    _inherit = "stock.lot"

    is_archived = fields.Boolean(
        default=False,
        help="Check this if you want to say this lot is archived (not inactive)",
    )
    is_archived_editable = fields.Boolean(
        compute="_compute_is_archived_editable",
    )

    @api.depends_context("uid")
    def _compute_is_archived_editable(self):
        if self.user_has_groups("stock.group_stock_manager"):
            self.update({"is_archived_editable": True})
        else:
            self.update({"is_archived_editable": False})
