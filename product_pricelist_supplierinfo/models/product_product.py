# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_supplierinfo_pricelist_price(
            self, rule, date=None, quantity=None):
        return self.product_tmpl_id._get_supplierinfo_pricelist_price(
            rule, date=date, quantity=quantity, product_id=self.id)

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

    def _select_seller(
            self, partner_id=False, quantity=0.0, date=None, uom_id=False,
            params=False):
        if not params or not params.get('avoid_min_qty'):
            return super()._select_seller(partner_id, quantity, date, uom_id, params)

        # Section based on the original Odoo's method '_select_seller' but in here the
        # validation of the min_qty on the seller is being avoided with the use of the
        # field `no_supplierinfo_min_quantity` on the model `product.pricelist.item`.
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)

        res = self.env['product.supplierinfo']
        sellers = self._prepare_sellers(params)
        company_id = self.env.context.get('force_company')
        if company_id:
            sellers = sellers.filtered(
                lambda s: not s.company_id or s.company_id.id == company_id)
        for seller in sellers:
            if (
                (not seller.date_start or seller.date_start <= date)
                and (not seller.date_end or seller.date_end >= date)
                and (not partner_id
                     or seller.name in [partner_id, partner_id.parent_id])
                and (not seller.product_id or seller.product_id == self)
            ):
                res |= seller
                break
        return res
