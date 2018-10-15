# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _get_price_from_supplierinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        supplierinfo = self.env['product.supplierinfo'].search(
            ['|', ('product_tmpl_id', '=', self.product_tmpl_id.id),
             ('product_id', '=', self.id),
             ('supplierinfo_type', '=', 'customer'),
             ('name', '=', partner_id)], limit=1)
        if supplierinfo:
            return supplierinfo.price
        return 0.0

    @api.multi
    def price_compute(
            self, price_type, uom=False, currency=False, company=False):
        if price_type == 'partner':
            partner = self.env.context.get('partner_id', False) or \
                self.env.context.get('partner', False)
            prices = super(ProductProduct, self).price_compute(
                'list_price', uom, currency, company)
            for product in self:
                price = product._get_price_from_supplierinfo(partner)
                if not price:
                    continue
                prices[product.id] = price
                if not uom and self._context.get('uom'):
                    uom = self.env['product.uom'].browse(self._context['uom'])
                if not currency and self._context.get('currency'):
                    currency = self.env['res.currency'].browse(
                        self._context['currency'])
                if uom:
                    prices[product.id] = product.uom_id._compute_price(
                        prices[product.id], uom)
                if currency:
                    prices[product.id] = product.currency_id.compute(
                        prices[product.id], currency)
            return prices
        return super(ProductProduct, self).price_compute(
            price_type, uom, currency, company)
