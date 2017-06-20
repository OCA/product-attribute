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
        names = []
        product_customer_code_obj = self.env['product.customer.code']
        # res = super(ProductProduct, self).name_get()
        partner_id = self._context.get('partner_id')
        # FIXME: get res without default code then loop over each result and insert customer ref
        if partner_id:
            for product in self:
                product_code = None
                no_default_code = None
                product_code = product_customer_code_obj.search([
                        ('product_id', '=', product.id),
                        ('partner_id', '=', partner_id)
                    ], limit=1)
                # Skip the part adding default code to the name
                if product_code:
                    no_default_code = product.with_context(display_default_code=False)
                    name = super(
                        ProductProduct, no_default_code or product).name_get()[0]
                    name = '[{}] - {}'.format(product_code.product_code, name)
                else:
                    name = super(
                        ProductProduct, product).name_get()[0]
                names.append(name)
        import ipdb
        ipdb.set_trace()
        return name
        # return names or super(ProductProduct, self).name_get()

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
            import ipdb
            ipdb.set_trace()
        return res
