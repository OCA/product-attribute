# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """Recompute price after calling the atomic super method for
        getting proper prices when based on supplier info.
        """
        rule_obj = self.env["product.pricelist.item"]
        result = super()._compute_price_rule(products_qty_partner, date, uom_id)
        # Make sure all rule records are fetched at once at put in cache
        rule_obj.browse(x[1] for x in result.values()).mapped("price_discount")
        for product, qty, _partner in products_qty_partner:
            rule = rule_obj.browse(result[product.id][1])
            if rule.compute_price == "formula" and rule.base == "supplierinfo":
                context = self.env.context
                result[product.id] = (
                    product._get_supplierinfo_pricelist_price(
                        rule,
                        date=date or context.get("date", fields.Date.today()),
                        quantity=qty,
                    ),
                    rule.id,
                )
        return result


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("supplierinfo", "Prices based on supplier info")],
        ondelete={"supplierinfo": "set default"},
    )
    no_supplierinfo_min_quantity = fields.Boolean(
        string="Ignore Supplier Info Min. Quantity",
    )
    filter_supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier filter",
        help="Only match prices from the selected supplier",
    )
