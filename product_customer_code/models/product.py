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

    def _get_customer_code(self):
        print('get customer code')
        print(self._context)
        product_customer_code_obj = self.env['product.customer.code']
        partner_id = self._context.get('partner_id')
        product_code = product_customer_code_obj.search([
            ('product_id', '=', self.id),
            ('partner_id', '=', partner_id)
        ], limit=1)
        return (
            product_code.product_code if product_code
            else None
        )

    @api.one
    def _compute_product_code(self):
        code = self._get_customer_code()
        if not code:
            return super(ProductProduct, self)._compute_product_code()
        self.code = code

    @api.multi
    def name_get(self):
        print('name_get')
        print(self._context)
        partner_id = self._context.get('partner_id')
        product_customer_code_obj = self.env['product.customer.code']
        show_customer_code = self._context.get('show_customer_code', True)
        display_default_code = self._context.get('display_default_code', True)
        # replace 'default code' by customer code
        if show_customer_code and display_default_code and partner_id:
            no_default_code = self.with_context(display_default_code=False)
            # get product names without codes
            res = super(ProductProduct, no_default_code).name_get()
            # res is [(product_id, name)...]
            dict_res = dict(res)
            new_res = []
            for product in self:
                name = dict_res[product.id]
                if product.code:
                    name = u'[{}] - {}'.format(product.code, name)
                new_res.append((product.id, name))
            return new_res
        return super(ProductProduct, self).name_get()

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Shows products with matching customer code
        """
        no_customer_code = self.with_context(show_customer_code=False)
        res = super(ProductProduct, no_customer_code).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # import ipdb
        # ipdb.set_trace()
        if (len(res) < limit):
            partner_id = self._context.get('partner_id')
            if partner_id:
                product_customer_code_obj = self.env['product.customer.code']
                product_codes = product_customer_code_obj.search([
                    ('product_code', operator, name),
                    ('partner_id', '=', partner_id)
                ], limit=limit)
                # get product names for all product customer code
                # matching the query
                res.extend(
                    product_codes.with_context(partner_id=partner_id).mapped('product_id').name_get())
        return res
