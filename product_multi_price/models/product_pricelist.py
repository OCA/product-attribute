# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """Recompute price after calling the atomic super method for
        getting proper prices when based on multi price.
        """
        rule_obj = self.env["product.pricelist.item"]
        result = super()._compute_price_rule(products_qty_partner, date, uom_id)
        # Make sure all rule records are fetched at once and put in cache
        rule_obj.browse(x[1] for x in result.values()).mapped("price_discount")
        for product, _qty, _partner in products_qty_partner:
            rule = rule_obj.browse(result[product.id][1])
            if rule.compute_price == "formula" and rule.base == "multi_price":
                result[product.id] = (
                    product._get_multiprice_pricelist_price(rule),
                    rule.id,
                )
        return result


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("multi_price", "Other Price")],
    )
    multi_price_name = fields.Many2one(
        comodel_name="product.multi.price.name",
        string="Other Price Name",
    )
