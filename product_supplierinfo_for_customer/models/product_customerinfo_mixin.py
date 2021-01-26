# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSupplierInfoMixin(models.AbstractModel):
    _name = 'product.customerinfo.mixin'
    _description = 'Common methods to compute prices based on partners'

    def _get_price_from_customerinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        if self._name == "product.template":
            domain = [
                ("name", "=", partner_id),
                ("product_tmpl_id", "=", self.id),
            ]
        else:
            domain = [
                ("name", "=", partner_id),
                "|",
                ("product_id", "=", self.id),
                "&",
                ("product_tmpl_id", "=", self.product_tmpl_id.id),
                ("product_id", "=", False),
            ]
        customerinfo = self.env["product.customerinfo"].sudo().search(
            domain, limit=1, order="product_id, sequence",)
        if customerinfo:
            return customerinfo.price
        return 0.0

    def get_customerinfo_price(
            self, uom=False, currency=False, company=False):
        partner_id = self.env.context.get('partner_id', False) or \
            self.env.context.get('partner', False)
        if partner_id and isinstance(partner_id, models.BaseModel):
            partner_id = partner_id.id
        prices = self.price_compute('list_price', uom, currency, company)
        for product in self:
            price = product._get_price_from_customerinfo(partner_id)
            if not price:
                continue
            prices[product.id] = price
            if not uom and self._context.get('uom'):
                uom = self.env['uom.uom'].browse(self._context['uom'])
            if not currency and self._context.get('currency'):
                currency = self.env['res.currency'].browse(
                    self._context['currency'])
            if uom:
                prices[product.id] = product.uom_id._compute_price(
                    prices[product.id], uom)
            if currency:
                date = self.env.context.get('date', fields.Datetime.now())
                prices[product.id] = product.currency_id._convert(
                    prices[product.id], currency, company, date)
        return prices
