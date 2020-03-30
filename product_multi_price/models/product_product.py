# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields, tools
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    price_ids = fields.One2many(
        comodel_name='product.multi.price',
        inverse_name='product_id',
    )
    multi_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute='_compute_multi_price',
        groups="base.group_user",
    )

    def _get_multiprice_pricelist_price(self, rule):
        """Method for getting the price from multi price."""
        self.ensure_one()
        company = rule.company_id or self.env.user.company_id
        price = self.env['product.multi.price'].search([
            ('company_id', '=', company.id),
            ('name', '=', rule.multi_price_name.id),
            ('product_id', '=', self.id),
        ]).price or 0
        if price:
            # We have to replicate this logic in this method as pricelist
            # method are atomic and we can't hack inside.
            # Verbatim copy of part of product.pricelist._compute_price_rule.
            qty_uom_id = self._context.get('uom') or self.uom_id.id
            price_uom = self.env['product.uom'].browse([qty_uom_id])
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

    def _compute_multi_price(self):
        """Use multi_price field as the proxy for any of the registered
           multi price fields on the product passing it by context"""
        multi_price_field = self.env.context.get('multi_price_field', False)
        if not multi_price_field:
            self.update({'multi_price': 0})
            return
        prices_list = self.env['product.multi.price'].search_read([
            ('name.name', '=', multi_price_field),
            ('product_id', 'in', self.ids),
            ('company_id', '=', self.env.user.company_id.id)
        ], ['product_id', 'price'], limit=1)
        prices_dict = {x['product_id'][0]: x['price'] for x in prices_list}
        for product in self:
            product.multi_price = prices_dict.get(product.id, 0.0)
