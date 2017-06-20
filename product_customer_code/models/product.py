# -*- coding: utf-8 -*-
# Copyright 2012 Vauxoo - http://www.vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_customer_code_ids = fields.One2many(
        comodel_name='product.customer.code',
        inverse_name='product_id',
        string='Customer Codes',
        copy=False
    )

    @api.multi
    def name_get(self):
        product_customer_code_obj = self.env['product.customer.code']
        partner_id = self._context.get('partner_id')
        if self._context.get('display_default_code', True) and partner_id:
            no_default_code = self.with_context(display_default_code=False)
            res = super(ProductProduct, no_default_code).name_get()
            new_res = []
            for (product_id, name) in res:
                new_name = ''
                product = self.browse(product_id)
                product_code = product_customer_code_obj.search([
                    ('product_id', '=', product.id),
                    ('partner_id', '=', partner_id)
                ], limit=1)
                product_code = getattr(product_code, 'product_code', None) or product.code
                if product_code:
                    new_name = '[{}] - {}'.format(product_code, name)
                new_res.append((product_id, new_name or name))
            return new_res
        return super(ProductProduct, self).name_get()

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        res = super(ProductProduct, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if (len(res) < limit):
            partner_id = self._context.get('partner_id')
            if partner_id:
                product_customer_code_obj = self.env['product.customer.code']
                product_codes = product_customer_code_obj.search([
                    ('product_code', operator, name),
                    ('partner_id', '=', partner_id)
                ], limit=limit)
                res.extend(product_codes.mapped('product_id').name_get())
            # import ipdb
            # ipdb.set_trace()
        return res
