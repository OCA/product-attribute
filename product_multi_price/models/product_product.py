# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields, tools, api, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    price_ids = fields.One2many(
        comodel_name='product.multi.price',
        inverse_name='product_id',
        string="Other Prices",
    )

    @api.multi
    @api.constrains('price_ids')
    def _check_price_ids(self):
        for p in self:
            for price in p.price_ids:
                prices = price.search([
                    ('name', '=', price.name.id),
                    ('product_id', '=', price.product_id.id),
                ])
                if len(prices) > 1:
                    raise ValidationError(_(
                        "You can't have prices with the same name"))

    def _get_multiprice_pricelist_price(self, rule):
        """Method for getting the price from multi price."""
        self.ensure_one()
        price = self.env['product.multi.price'].search([
            ('name', '=', rule.multi_price_name.id),
            ('product_id', '=', self.id),
        ]).price or 0
        if price:
            # We have to replicate this logic in this method as pricelist
            # method are atomic and we can't hack inside.
            # Verbatim copy of part of product.pricelist._compute_price_rule.
            qty_uom_id = self._context.get('uom') or self.uom_id.id
            price_uom = self.env['uom.uom'].browse([qty_uom_id])
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
        """Return temporary prices when computation is done for multi price for
        avoiding error on super method. We will later fill these with the
        correct values.
        """
        if price_type == 'multi_price':
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
