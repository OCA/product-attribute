#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _is_products_pricelist_item(self):
        """This price rule will update product prices when updated."""
        self.ensure_one()
        company = self.company_id or self.env.company
        company_pricelist = company.products_price_pricelist_id
        return (
            self.pricelist_id == company_pricelist
            and self.compute_price == "fixed"
            and self.applied_on
            in [
                "1_product",
                "0_product_variant",
            ]
        )

    def _update_products_pricelist_prices(self):
        """If the items are in the company pricelist, update price of matching products."""
        for item in self:
            if item._is_products_pricelist_item():
                price = item.fixed_price
                if item.applied_on == "1_product":
                    item.product_tmpl_id.list_price = price
                elif item.applied_on == "0_product_variant":
                    item.product_id.lst_price = price

    @api.model_create_multi
    def create(self, vals_list):
        items = super().create(vals_list)
        items._update_products_pricelist_prices()
        return items

    def write(self, vals):
        res = super().write(vals)
        self._update_products_pricelist_prices()
        return res
