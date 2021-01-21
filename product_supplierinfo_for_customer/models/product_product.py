# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = ['product.product', 'product.customerinfo.mixin']
    _name = 'product.product'

    @api.multi
    def name_get(self):
        res = super(ProductProduct, self.with_context(customerinfo=True)).\
            name_get()
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100,
                     name_get_uid=None):
        res = super(ProductProduct, self)._name_search(
            name, args=args, operator=operator, limit=limit,
            name_get_uid=name_get_uid)
        if not limit or len(res) >= limit:
            limit = (limit - len(res)) if limit else False
        if (not name and limit or not self._context.get('partner_id') or
                len(res) >= limit):
            return res
        limit -= len(res)
        customerinfo_ids = self.env['product.customerinfo']._search(
            [('name', '=', self._context.get('partner_id')), '|',
             ('product_code', operator, name),
             ('product_name', operator, name)], limit=limit,
            access_rights_uid=name_get_uid)
        if not customerinfo_ids:
            return res
        res_templates = self.browse(
            [product_id for product_id, _name in res]
        ).mapped('product_tmpl_id')
        product_tmpls = self.env['product.customerinfo'].browse(
            customerinfo_ids).mapped('product_tmpl_id') - res_templates
        product_ids = self._search(
            [('product_tmpl_id', 'in', product_tmpls.ids)], limit=limit,
            access_rights_uid=name_get_uid)
        res.extend(self.browse(product_ids).name_get())
        return res

    @api.multi
    def price_compute(
            self, price_type, uom=False, currency=False, company=False):
        if price_type == 'partner':
            return self.get_customerinfo_price(uom, currency, company)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
