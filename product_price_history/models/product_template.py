from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    price_history_count = fields.Integer(compute="_compute_price_history_count")

    def _compute_price_history_count(self):
        for t in self:
            t.price_history_count = self.env["product.price.history"].search_count(
                [("product_tmpl_id", "=", t.id)]
            )
