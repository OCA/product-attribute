# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _get_pricelist_item_name_price(self):
        res = super(). _get_pricelist_item_name_price()
        for record in self.filtered("product_id"):
            record.name = record.product_id.display_name
        for record in self.filtered("product_tmpl_id"):
            record.name = record.product_tmpl_id.display_name
        return res
