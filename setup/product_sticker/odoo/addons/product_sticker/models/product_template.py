from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_view_stickers(self):
        """Action to open the Stickers related to this Product Template"""
        stickers = self.get_product_stickers()
        action = self.env.ref("product_sticker.action_product_sticker").read()[0]
        action["domain"] = [("id", "in", stickers.ids)]
        return action

    def _get_sticker_arguments(self):
        no_variant_attribute_lines = self.attribute_line_ids.filtered(
            lambda al: al.attribute_id.create_variant == "no_variant"
        )
        return {
            "categories": self.categ_id,
            "attributes": no_variant_attribute_lines.attribute_id,
            "attribute_values": no_variant_attribute_lines.value_ids,
        }

    @api.returns("product.sticker")
    def get_product_stickers(self):
        """Attribute Stickers related to this Product Template and its variants"""
        return self.env["product.sticker"]._get_stickers(
            **self._get_sticker_arguments()
        )
