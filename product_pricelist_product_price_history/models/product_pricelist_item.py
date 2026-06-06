# Copyright 2026 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def write(self, vals):
        if "fixed_price" in vals:
            for item in self:
                new_price = vals.get("fixed_price")
                if item.fixed_price != new_price and (
                    item.product_id or item.product_tmpl_id
                ):
                    self.env["product.pricelist.item.history"].create(
                        {
                            "product_id": item.product_tmpl_id.product_variant_id.id
                            or item.product_id.id,
                            "pricelist_id": item.pricelist_id.id,
                            "old_price": item.fixed_price,
                            "new_price": new_price,
                        }
                    )
        return super().write(vals)
