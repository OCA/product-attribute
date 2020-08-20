# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_supplierinfo_pricelist_price(
            self, rule, date=None, quantity=None, product_id=None):
        """Method for getting the price from supplier info."""
        self.ensure_one()
        if product_id:
            domain = [
                '|',
                ('product_id', '=', product_id),
                ('product_tmpl_id', '=', self.id),
            ]
        else:
            domain = [
                ('product_tmpl_id', '=', self.id),
            ]
        if not rule.no_supplierinfo_min_quantity and quantity:
            domain += [
                '|',
                ('min_qty', '=', False),
                ('min_qty', '<=', quantity),
            ]
        if date:
            domain += [
                '|',
                ('date_start', '=', False),
                ('date_start', '<=', date),
                '|',
                ('date_end', '=', False),
                ('date_end', '>=', date),
            ]
        # We use a different default order because we are interested in getting
        # the price for lowest minimum quantity if no_supplierinfo_min_quantity
        supplierinfos = self.env['product.supplierinfo'].search(
            domain, order='min_qty,sequence,price',
        )
        if rule.no_supplierinfo_min_quantity:
            selected_supplierinfo = supplierinfos[:1]
        else:
            selected_supplierinfo = supplierinfos[-1:]
        price = selected_supplierinfo._get_supplierinfo_pricelist_price()
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
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == 'supplierinfo':
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
