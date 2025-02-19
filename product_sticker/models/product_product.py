from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_stickers(self):
        """Action to open the Stickers related to this Product"""
        stickers = self.get_product_stickers()
        action = self.env.ref("product_sticker.action_product_sticker").read()[0]
        action["domain"] = [("id", "in", stickers.ids)]
        return action

    @api.returns("product.sticker")
    def get_product_stickers(self, extra_domain=None):
        """Product Stickers related to this Product Variant and
        its Template for certain models"""
        return self.env["product.sticker"]._get_stickers(
            self,
            extra_domain=extra_domain,
        )
