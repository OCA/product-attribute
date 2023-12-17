from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    price_history_count = fields.Integer(compute="_compute_price_history_count")

    def _compute_price_history_count(self):
        for p in self:
            p.price_history_count = self.env["product.price.history"].search_count(
                [("product_id", "=", p.id)]
            )
