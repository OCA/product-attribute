from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_stickers(self):
        """Action to open the Stickers related to this Product"""
        stickers = self.get_product_stickers()
        action = self.env.ref("product_sticker.action_product_sticker").read()[0]
        action["domain"] = [("id", "in", stickers.ids)]
        return action

    def _get_sticker_arguments(self):
        pavs = self.product_template_variant_value_ids.product_attribute_value_id
        return {
            "categories": self.categ_id,
            "attributes": pavs.attribute_id,
            "attribute_values": pavs,
        }

    @api.returns("product.sticker")
    def get_product_stickers(self):
        """Product Stickers related to this Product Variant and its Template"""
        # Product Template: Common stickers
        pt_stickers = self.product_tmpl_id.get_product_stickers()
        # Product Product: Specific stickers
        pp_stickers = self.env["product.sticker"]._get_stickers(
            **self._get_sticker_arguments()
        )
        return pt_stickers | pp_stickers
