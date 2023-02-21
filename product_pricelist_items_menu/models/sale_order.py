from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def update_prices(self):
        self.ensure_one()
        for line in self._get_update_prices_lines():
            self.env["product.product"].invalidate_cache()
            line.product_uom_change()
            line.discount = 0
            line._onchange_discount()
        self.show_update_pricelist = False
        self.message_post(
            body=_(
                "Product prices have been recomputed according to pricelist <b>%s<b> ",
                self.pricelist_id.display_name,
            )
        )
