# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo import fields, models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_supplierinfo_pricelist_price(
            self, rule, date=None, quantity=None, product_id=None):
        """Method for getting the price from supplier info."""
        self.ensure_one()
        price = 0.0
        product = self.product_variant_id
        if product_id:
            product = product.browse(product_id)
        if rule.no_supplierinfo_min_quantity:
            quantity = 1.0
        # The product_variant_id returns empty recordset if template is not
        # active, so we must ensure variant exists or _select_seller fails.
        if product:
            if type(date) == datetime:
                date = date.date()
            seller = product._select_seller(
                partner_id=rule.filter_supplier_id,
                quantity=quantity,
                date=date)
            if seller:
                price = seller._get_supplierinfo_pricelist_price()
        if price:
            # We need to convert the price if the pricelist and seller have
            # different currencies so the price have the pricelist currency
            if rule.currency_id != seller.currency_id:
                convert_date = date or self.env.context.get(
                    'date', fields.Date.today())
                price = seller.currency_id._convert(
                    price, rule.currency_id, seller.company_id, convert_date)

            # We have to replicate this logic in this method as pricelist
            # method are atomic and we can't hack inside.
            # Verbatim copy of part of product.pricelist._compute_price_rule.
            qty_uom_id = self._context.get('uom') or self.uom_id.id
            price_uom = self.env['uom.uom'].browse([qty_uom_id])

            # We need to convert the price to the uom used on the sale, if the
            # uom on the seller is a different one that the one used there.
            if seller and seller.product_uom != price_uom:
                price = seller.product_uom._compute_price(price, price_uom)

            convert_to_price_uom = (
                lambda price: self.uom_id._compute_price(
                    price, price_uom))
            price_limit = price
            price = (price - (price * (rule.price_discount / 100))) or 0.0
            if rule.price_round:
                price = tools.float_round(
                    price, precision_rounding=rule.price_round)
            if rule.price_surcharge:
                price_surcharge = convert_to_price_uom(rule.price_surcharge)
                price += price_surcharge
            if rule.price_min_margin:
                price_min_margin = convert_to_price_uom(rule.price_min_margin)
                price = max(price, price_limit + price_min_margin)
            if rule.price_max_margin:
                price_max_margin = convert_to_price_uom(rule.price_max_margin)
                price = min(price, price_limit + price_max_margin)
        return price

    def price_compute(self, price_type, uom=False, currency=False,
                      company=False):
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == 'supplierinfo':
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
