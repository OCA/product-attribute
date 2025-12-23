# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    alternative_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        relation="product_pricelist_alternative_rel",
        column1="origin_id",
        column2="alternative_id",
        domain="[('id', '!=', id)]",
    )
    is_alternative_to_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        relation="product_pricelist_alternative_rel",
        column1="alternative_id",
        column2="origin_id",
    )
    is_alternative_to_pricelist_count = fields.Integer(
        compute="_compute_is_alternative_to_pricelist_count"
    )

    @api.depends("is_alternative_to_pricelist_ids")
    def _compute_is_alternative_to_pricelist_count(self):
        groups = self._read_group(
            [("alternative_pricelist_ids", "in", self.ids)],
            ["alternative_pricelist_ids"],
            ["__count"],
        )
        data = {pricelist.id: count for pricelist, count in groups}
        for pricelist in self:
            pricelist.is_alternative_to_pricelist_count = data.get(pricelist.id, 0)

    def action_view_is_alternative_to_pricelist(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": self.env._("Is Alternative to Pricelist"),
            "res_model": "product.pricelist",
            "view_mode": "list,form",
            "domain": [("id", "in", self.is_alternative_to_pricelist_ids.ids)],
            "context": dict(self.env.context, create=False),
        }
        if self.is_alternative_to_pricelist_count == 1:
            action.update(
                {"view_mode": "form", "res_id": self.is_alternative_to_pricelist_ids.id}
            )
        return action

    def _get_alternative_pricing_product(self, product):
        """Return the product to use for alternative pricing."""
        if product._name != "product.template":
            return product
        combination_ids = product.env.context.get(
            "product_pricelist_alternative_combination_ids"
        )
        if not combination_ids:
            return product
        combination = product.env["product.template.attribute.value"].browse(
            combination_ids
        )
        variant = product._get_variant_for_combination(combination)
        return variant or product

    def _compute_price_rule(
        self,
        products,
        quantity,
        *,
        currency=None,
        uom=None,
        date=False,
        compute_price=True,
        **kwargs,
    ):
        # OVERRIDE: to compare the regular price with alternative pricelists
        # and keep the lower price when the pricelist item policy allows it.
        # This context key is used in `sale.order::_recompute_prices()`,
        # triggered by `action_update_prices()` button that recomputes
        # the unit price of all products based on the new pricelist.
        if self.env.context.get("force_price_recomputation"):
            compute_price = True

        price_date = date or fields.Datetime.now()
        res = super()._compute_price_rule(
            products,
            quantity,
            currency=currency,
            uom=uom,
            date=price_date,
            compute_price=compute_price,
            **kwargs,
        )
        # In some contexts we want to ignore alternative pricelists
        # and return the original price
        if self.env.context.get("skip_alternative_pricelist", False):
            return res

        effective_currency = (
            currency or self.currency_id or self.env.company.currency_id
        )
        for product in products:
            reference_pricelist_item = self.env["product.pricelist.item"].browse(
                res[product.id][1]
            )
            policy = reference_pricelist_item.alternative_pricelist_policy
            if policy == "use_lower_price":
                # When ``compute_price=False``, Odoo returns the matched rule
                # with a 0.0 price placeholder:
                # ``{product.id: (0.0, matched_rule_id)}``.
                # Keep `res` as the official return payload, but compute the
                # regular pricelist price from the matched rule so lower-price
                # alternatives can be compared.
                if compute_price:
                    regular_price = res[product.id][0]
                else:
                    regular_price = reference_pricelist_item._compute_price(
                        product,
                        quantity,
                        uom or product.uom_id,
                        date=price_date,
                        currency=effective_currency,
                        **kwargs,
                    )
                # If a product template with variants is selected on the sale
                # order line and the sale configurator is opened, resolve the
                # selected combination to ensure variant specific lower price
                # alternative rules can match.
                alternative_product = self._get_alternative_pricing_product(product)
                for alternative_pricelist in self.alternative_pricelist_ids:
                    # Always compute real alternative prices, because
                    # lower price selection requires actual prices.
                    alternative_price_rule = alternative_pricelist._compute_price_rule(
                        alternative_product,
                        quantity,
                        currency=currency,
                        uom=uom,
                        date=price_date,
                        compute_price=True,
                        **kwargs,
                    )
                    alternative_result = alternative_price_rule[alternative_product.id]
                    # Since 19.0, price fields can display more decimals with
                    # min_display_digits="Product Price", but no rounding is
                    # enforced on the stored values. Compare raw unit prices so
                    # sub-cent alternative prices can still be selected.
                    if alternative_result[0] < regular_price:
                        # Keep the current best price updated so the next
                        # alternative is compared against the lowest price
                        # found so far. In rule only mode, keep the official
                        # 0.0 price placeholder and return only the winning
                        # rule id.
                        regular_price = alternative_result[0]
                        if compute_price:
                            res[product.id] = alternative_result
                        else:
                            res[product.id] = (
                                res[product.id][0],
                                alternative_result[1],
                            )
        return res

    @api.constrains("alternative_pricelist_ids")
    def _check_pricelist_alternative_items_based_on_other_pricelist(self):
        """Alternative pricelists can not contain items based on other pricelist"""
        for pricelist in self:
            if pricelist.alternative_pricelist_ids.item_ids.filtered(
                lambda item: item.compute_price == "formula"
                and item.base == "pricelist"
            ):
                raise ValidationError(
                    self.env._(
                        "Formulas based on another pricelist are not allowed "
                        "on alternative pricelists."
                    )
                )
