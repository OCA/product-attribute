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
