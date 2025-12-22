from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    indirect_cost_percent = fields.Float(string="Indirect Cost %", digits=(16, 2))
    indirect_cost_amount = fields.Float(
        digits=(16, 2),
        compute="_compute_indirect_cost_amount",
        store=True,
    )

    @api.depends("indirect_cost_percent", "price")
    def _compute_indirect_cost_amount(self):
        for record in self:
            record.indirect_cost_amount = (
                record.price * record.indirect_cost_percent / 100
                if record.price and record.indirect_cost_percent
                else 0.0
            )
