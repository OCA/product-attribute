# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    sale_price = fields.Float(
        'Sale Price', digits=dp.get_precision('Sale Price'),
        help="Sale Price suggested by supplier")

    @api.multi
    def _update_supplier_sale_price(self):
        product_obj = self.env['product.product']
        self.ensure_one()

        products = product_obj.browse()
        if self.product_id:
            products = self.product_id
        elif self.product_tmpl_id:
            products = product_obj.search([
                ('product_tmpl_id', '=', self.product_tmpl_id.id),
            ])
        for product in products:
            product_vals = product._prepare_supplier_sale_price()
            product.write(product_vals)

    @api.model
    def create(self, vals):
        new_supplierinfo = super(ProductSupplierinfo, self).create(vals)
        if vals.get('sale_price'):
            new_supplierinfo._update_supplier_sale_price()
        return new_supplierinfo

    @api.multi
    def write(self, vals):
        res = super(ProductSupplierinfo, self).write(vals)

        if vals.get('sale_price'):
            for supplierinfo in self:
                supplierinfo._update_supplier_sale_price()

        return res

    @api.multi
    def unlink(self):
        product_obj = self.env['product.product']

        product_ids = []
        product_tmpl_ids = []
        for supplierinfo in self:
            if supplierinfo.product_id:
                product_ids.append(supplierinfo.product_id.id)
            elif supplierinfo.product_tmpl_id:
                product_tmpl_ids.append(supplierinfo.product_tmpl_id.id)
        res = super(ProductSupplierinfo, self).unlink()

        products_without_seller = product_obj.search([
            ('seller_ids', '=', False),
            '|',
            ('product_tmpl_id', 'in', product_tmpl_ids),
            ('id', 'in', product_ids),
        ])
        products_without_seller.write({
            'use_supplier_sale_price': False,
        })

        return res
