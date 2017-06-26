# coding: utf-8
# Copyright 2017 Vauxoo (https://www.vauxoo.com) info@vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    product_customer_code_ids = fields.One2many(
        'product.customer.code', 'product_id', string='Product customer codes',
        copy=False, help="Different codes that has the product for each "
        "partner.")

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=80):
        res = super(ProductProduct, self).name_search(
            name, args=args, operator=operator, limit=limit)
        if res or not self._context.get('partner_id'):
            return res
        partner_id = self._context['partner_id']
        product_customer_code_obj = self.env['product.customer.code']
        prod_code_ids = product_customer_code_obj.search(
            [('product_code', '=', name),
             ('partner_id', '=', partner_id)], limit=limit)
        # TODO: Search for product customer name
        res = prod_code_ids.mapped('product_id').name_get()
        return res
