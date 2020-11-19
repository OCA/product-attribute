# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    supplier_discount_ids = fields.One2many(
        'product.brand.supplier.discount', 'product_brand_id',
        string='Suppliers')


class ProductBrandSupplierDiscount(models.Model):
    _name = 'product.brand.supplier.discount'

    product_brand_id = fields.Many2one('product.brand', string='Supplier')
    partner_id = fields.Many2one('res.partner', string='Supplier')
    discount = fields.Float(
        string='Discount (%)', digits=dp.get_precision('Discount'), default=.0)
