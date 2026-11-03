from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_view_stickers(self):
        """Action to open the Stickers related to this Product Template"""
        stickers = self.product_variant_ids.get_product_stickers()
        action = self.env.ref("product_sticker.action_product_sticker").read()[0]
        action["domain"] = [("id", "in", stickers.ids)]
        return action
