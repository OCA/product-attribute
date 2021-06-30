# Copyright 2021 - Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CostAdjustmentLine(models.Model):
    _inherit = "cost.adjustment.line"

    mrp_production_ids = fields.Many2many(
        "mrp.production", string="Manufacturing Orders"
    )

    @api.onchange("product_id", "product_original_cost", "product_cost", "state")
    def _set_productions(self):
        for line in self:
            if line.state not in ("posted"):
                if line.mrp_production_ids:
                    line.mrp_production_ids = [(5)]
                producton_ids = self.env["mrp.production"].search(
                    [("state", "in", ["draft", "confirmed", "progress"])]
                )
                for production in producton_ids:
                    components = production.move_raw_ids.mapped("product_id")
                    for product in components:
                        if line.product_id.id == product.id:
                            line.mrp_production_ids = [(4, production.id)]

    def action_view_production(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("mrp.mrp_production_action")
        action["domain"] = [("id", "in", self.mapped("mrp_production_ids.id"))]
        action["context"] = dict(self._context, create=False)
        return action
