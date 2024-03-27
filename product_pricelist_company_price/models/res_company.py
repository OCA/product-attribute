#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    products_price_pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Products Pricelist",
        help="Prices set for individual products in this pricelist "
        "propagate to the sales price of the products it affects.",
    )

    def write(self, vals):
        res = super().write(vals)
        if "products_price_pricelist_id" in vals:
            for company in self:
                products_pricelist = company.products_price_pricelist_id
                if products_pricelist:
                    products_pricelist.item_ids._update_products_pricelist_prices()
        return res
