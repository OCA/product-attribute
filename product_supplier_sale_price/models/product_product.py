# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import statistics

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    use_supplier_sale_price = fields.Boolean('Use Supplier Sale Price',
                                             default=True)

    supplier_sale_price = fields.Float(
        'Supplier_sale_price', compute='_compute_supplier_sale_price',
        readonly=True)

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

    @api.multi
    @api.depends('fix_price', 'use_supplier_sale_price',
                 'variant_seller_ids.sale_price')
    def _compute_lst_price(self):
        computed_lst_price_products = self.browse()
        for product in self:
            if product.use_supplier_sale_price:
                product.lst_price = product.supplier_sale_price
            else:
                computed_lst_price_products |= product
        super(ProductProduct, computed_lst_price_products)._compute_lst_price()

    @api.multi
    def _prepare_supplier_sale_price(self, force=False):
        self.ensure_one()

        vals = {}
        supplier_sale_price = self.supplier_sale_price
        if (force or self.use_supplier_sale_price) and supplier_sale_price:
            vals = {
                'lst_price': supplier_sale_price,
                'fix_price': supplier_sale_price,
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
            if 'fix_price' in vals\
                    and not self._context.get('update_price_list', False)\
                    and not self._context.get('update_fix_price', False):
                for product in self:
                    if len(product.product_tmpl_id.product_variant_ids) == 1\
                            and not product.use_supplier_sale_price:
                        product.product_tmpl_id.with_context(
                            update_price_list=True).write({
                                'list_price': vals['fix_price'],
                            })
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
