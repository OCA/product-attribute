from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_product_price_context(self):
        """Extend to make sure the partner context is set for price computation."""
        self.ensure_one()
        context = super()._get_product_price_context()
        # Add partner_id to the context
        if self.order_id.partner_id:
            context.update({"partner_id": self.order_id.partner_id.id})
        return context
