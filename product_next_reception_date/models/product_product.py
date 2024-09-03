# Copyright 2024 Akretion (http://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    date_next_reception = fields.Date(
        compute="_compute_date_next_reception", compute_sudo=True
    )

    def _compute_date_next_reception(self):
        pickings = self.env["stock.picking"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("product_id", "in", self.ids),
                ("picking_type_id.code", "=", "incoming"),
                ("state", "in", ["ready", "waiting", "assigned"]),
            ],
            limit=1,
        )
        picking_dict = {
            picking.product_id.id: picking.scheduled_date for picking in pickings
        }
        for record in self:
            record.date_next_reception = picking_dict.get(record.id, False)
