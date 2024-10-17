# Copyright 2024 Binhex - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_round


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """Apply overcharge to the price when applicable."""
        rule_obj = self.env["product.pricelist.item"]
        result = super()._compute_price_rule(products_qty_partner, date, uom_id)
        for product, _qty, _partner in products_qty_partner:
            rule = rule_obj.browse(result[product.id][1])
            if rule.overcharge:
                for overcharge in rule.overcharge_item_ids:
                    price = result[product.id][0]
                    if overcharge.can_be_apply(price):
                        result[product.id] = (
                            overcharge.apply_overcharge(price),
                            rule.id,
                        )
                        break
        return result


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    overcharge = fields.Boolean(
        string="Apply overcharge to the final price",
    )
    overcharge_item_ids = fields.One2many(
        "product.pricelist.overcharge.item",
        "item_id",
        "Overcharge Items",
        help="Only match prices from the selected supplier",
        copy=True,
    )


class ProductPricelistOverchargeItem(models.Model):
    _name = "product.pricelist.overcharge.item"

    sequence = fields.Integer(string="Sequence", default=1)
    item_id = fields.Many2one(
        "product.pricelist.item",
        "Pricelist Item",
        ondelete="cascade",
    )
    applied_on = fields.Selection(
        [
            ("allways", "Allways"),
            ("equal", "Equal than"),
            ("smaller", "Smaller/Equal than"),
            ("bigger", "Bigger/Equal than"),
            ("between", "Between"),
        ],
        "Apply",
        default="allways",
        required=True,
        help="Overcharge applicable on selected option",
    )
    min_price = fields.Float(
        "Min price",
        digits="Product Price",
        help="Minimal price to apply the overcharge.",
    )
    max_price = fields.Float(
        "Max price",
        digits="Product Price",
        help="Maximun price to apply the overcharge.",
    )
    overcharge_surcharge = fields.Float(
        "Overcharge Surcharge",
        digits="Product Price",
        help="Specify the fixed amount to add or subtract(if negative) to the result amount",
    )
    overcharge_discount = fields.Float("Overcharge Discount", default=0, digits=(16, 2))
    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        readonly=True,
        related="item_id.currency_id",
        store=True,
    )

    @api.constrains("min_price", "max_price")
    def _check_margin(self):
        if any(
            overc_item.applied_on == "between"
            and overc_item.min_price > overc_item.max_price
            for overc_item in self
        ):
            raise ValidationError(
                _("The minimum price should be lower than the maximum price.")
            )
        return True

    def can_be_apply(self, price):
        """Check if the overcharge is applicable"""
        self.ensure_one()
        if hasattr(self, "%s_can_be_apply" % self.applied_on):
            return getattr(self, "%s_can_be_apply" % self.applied_on)(price)

    def allways_can_be_apply(self, price):
        self.ensure_one()
        return True

    def equal_can_be_apply(self, price):
        self.ensure_one()
        return (
            float_compare(
                price, self.min_price, precision_rounding=self.currency_id.rounding
            )
            == 0
        )

    def smaller_can_be_apply(self, price):
        self.ensure_one()
        return (
            float_compare(
                price, self.max_price, precision_rounding=self.currency_id.rounding
            )
            <= 0
        )

    def bigger_can_be_apply(self, price):
        self.ensure_one()
        return (
            float_compare(
                price, self.min_price, precision_rounding=self.currency_id.rounding
            )
            >= 0
        )

    def between_can_be_apply(self, price):
        self.ensure_one()
        return (
            float_compare(
                price, self.max_price, precision_rounding=self.currency_id.rounding
            )
            <= 0
            and float_compare(
                price, self.min_price, precision_rounding=self.currency_id.rounding
            )
            >= 0
        )

    def apply_overcharge(self, price):
        """Apply overcharge"""
        self.ensure_one()
        price = (price - (price * (self.overcharge_discount / 100))) or 0.0
        if self.item_id.price_round:
            price = float_round(price, precision_rounding=self.item_id.price_round)
        price += self.overcharge_surcharge
        return price
