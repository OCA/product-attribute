# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_supplier_sale_price_computation = fields.Selection([
        ('more_expensive_sale_price', 'More Expensive Sale price'),
        ('cheapest_sale_price', 'Cheapest Sale price'),
        ('mean_sale_price', 'Mean Sale Price'),
        ('not_supplier_sale_price', 'Not Supplier Sale Price'),
        ], "Supplier Sale Price Computation",
        help="Choose how to compute supplier sale price")

    @api.model
    def get_values(self):
        param_obj = self.env['ir.config_parameter']

        res = super(ResConfigSettings, self).get_values()
        res.update(
            product_supplier_sale_price_computation=param_obj.sudo().get_param(
                'product_supplier_sale_price.field_res_config_settings_'
                '_product_supplier_sale_price_computation'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param_obj = self.env['ir.config_parameter']

        field = self.product_supplier_sale_price_computation or False

        param_obj.sudo().set_param(
            'product_supplier_sale_price.field_res_config_settings_'
            '_product_supplier_sale_price_computation', field)
