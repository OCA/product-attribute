# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import float_compare, float_is_zero

from ..utils import float_round


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_price(
        self, qty=1.0, pricelist=None, fposition=None, company=None, date=None
    ):
        """Computes the product prices

        :param qty:         The product quantity, used to apply pricelist rules.
        :param pricelist:   Optional. Get prices for a specific pricelist.
        :param fposition:   Optional. Apply fiscal position to product taxes.
        :param company:     Optional.
        :param date:        Optional.

        :returns: dict with the following keys:

            <value>                 The product unitary price
            <tax_included>          True if product taxes are included in <price>.

            If the pricelist.discount_policy is "without_discount":
            <original_value>        The original price (before pricelist is applied).
            <discount>              The discounted percentage.
        """
        self.ensure_one()
        AccountTax = self.env["account.tax"]
        # Apply company
        product = self.with_company(company) if company else self
        company = company or self.env.company
        # Always filter taxes by the company
        taxes = product.taxes_id.filtered(lambda tax: tax.company_id == company)
        # Apply fiscal position
        taxes = fposition.map_tax(taxes) if fposition else taxes
        # Set context. Some of the methods used here depend on these values
        product_context = dict(
            self.env.context,
            quantity=qty,
            pricelist=pricelist.id if pricelist else None,
            fiscal_position=fposition,
            date=date,
        )
        product = product.with_context(**product_context)
        pricelist = pricelist.with_context(**product_context) if pricelist else None
        price_unit = (
            pricelist._get_product_price(product, qty, date=date)
            if pricelist
            else product.lst_price
        )
        price_unit = AccountTax._fix_tax_included_price_company(
            price_unit, product.taxes_id, taxes, company
        )
        price_dp = self.env["decimal.precision"].precision_get("Product Price")
        price_unit = float_round(price_unit, price_dp)
        res = {
            "value": price_unit,
            "tax_included": any(tax.price_include for tax in taxes),
            # Default values in case price.discount_policy != "without_discount"
            "original_value": price_unit,
            "discount": 0.0,
        }
        if pricelist:
            rule_id = pricelist._get_product_rule(product, qty, date=date)
            pl_item = self.env["product.pricelist.item"].browse(rule_id)
            if not pl_item.exists():
                return res
            original_price_unit = product.lst_price
            if not pl_item._show_discount():
                # If the pricelist does not show the discount, we return the price as is
                if float_is_zero(original_price_unit, precision_digits=price_dp):
                    res["original_value"] = 0.0
                return res
            # Get the price rule
            price_unit, _ = pricelist._get_product_price_rule(product, qty, date=date)
            # Get the price before applying the pricelist
            price_dp = self.env["decimal.precision"].precision_get("Product Price")
            # Compute discount
            if not float_is_zero(
                original_price_unit, precision_digits=price_dp
            ) and float_compare(
                original_price_unit, price_unit, precision_digits=price_dp
            ):
                discount = (
                    (original_price_unit - price_unit) / original_price_unit * 100
                )
                # Apply the right precision on discount
                discount_dp = self.env["decimal.precision"].precision_get("Discount")
                discount = float_round(discount, discount_dp)
            else:
                discount = 0.00
            # Compute prices
            original_price_unit = AccountTax._fix_tax_included_price_company(
                original_price_unit, product.taxes_id, taxes, company
            )
            original_price_unit = float_round(original_price_unit, price_dp)
            res.update(
                {
                    "original_value": original_price_unit,
                    "discount": discount,
                }
            )
        return res
