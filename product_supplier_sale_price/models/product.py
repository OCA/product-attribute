# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import statistics

from odoo import models, fields, api, _
from odoo.exceptions import UserError
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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.depends('seller_ids.sale_price', 'use_supplier_sale_price')
    def _compute_supplier_sale_price(self):
        param_obj = self.env['ir.config_parameter']

        sale_price_computation = param_obj.sudo().get_param(
            'product_supplier_sale_price'
            '.field_res_config_settings_'
            '_product_supplier_sale_price_computation')

        for product in self:
            supplier_prices = []
            for seller in product.variant_seller_ids:
                if seller.sale_price\
                        and (seller.product_id.default_code ==
                             product.default_code
                             or (not seller.product_id and
                                 seller.product_tmpl_id ==
                                 product.product_tmpl_id)):
                    supplier_prices.append(seller.sale_price)
            if not supplier_prices:
                # this product has no supplier sale prices
                product.supplier_sale_price = 0.0
                continue
            if sale_price_computation == 'more_expensive_sale_price':
                sale_price = max(supplier_prices)
            elif sale_price_computation == 'cheapest_sale_price':
                sale_price = min(supplier_prices)
            elif sale_price_computation == 'mean_sale_price':
                sale_price = statistics.mean(supplier_prices)
            else:  # 'not_supplier_sale_price'
                sale_price = False
            product.supplier_sale_price = sale_price

    use_supplier_sale_price = fields.Boolean('Use Supplier Sale Price')

    supplier_sale_price = fields.Float(
        'Supplier_sale_price', compute='_compute_supplier_sale_price',
        readonly=True)

    @api.multi
    @api.depends('fix_price', 'use_supplier_sale_price',
                 'variant_seller_ids.sale_price')
    def _compute_lst_price(self):
        for product in self:
            if product.use_supplier_sale_price:
                product.lst_price = product.supplier_sale_price
            else:
                super(ProductProduct, product)._compute_lst_price()

    @api.multi
    def _prepare_supplier_sale_price(self, force=False):
        self.ensure_one()

        vals = {}
        supplier_sale_price = self.supplier_sale_price
        if (force or self.use_supplier_sale_price) and supplier_sale_price:
            vals = {
                'lst_price': self.supplier_sale_price,
                'fix_price': self.supplier_sale_price,
            }
        return vals

    @api.multi
    def write(self, vals):
        if vals.get('use_supplier_sale_price'):
            # For every product set its price
            for product in self:
                product_vals = vals.copy()
                product_vals.update(
                    product._prepare_supplier_sale_price(force=True))
                res = super(ProductProduct, product).write(product_vals)
        else:
            res = super(ProductProduct, self).write(vals)
        return res

    @api.onchange('use_supplier_sale_price')
    def _onchange_use_supplier_sale_price(self):
        param_obj = self.env['ir.config_parameter']
        if self.use_supplier_sale_price:
            sale_price_computation = param_obj.sudo().get_param(
                'product_supplier_sale_price'
                '.field_res_config_settings_'
                '_product_supplier_sale_price_computation')
            if sale_price_computation == 'not_supplier_sale_price':
                raise UserError(
                    _('Supplier Sale Price Computation is set to: '
                      'No to use supplier price. '
                      'Please choose a computation mode in Sale Settings'))
            if not self.supplier_sale_price:
                raise UserError(
                    _('This product has no sale prices suggested'
                      ' by its suppliers'))
            self.fix_price = self.supplier_sale_price
