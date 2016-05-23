# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_customer_code_ids = fields.One2many(
        string='Customer Codes',
        comodel_name='product.customer.code',
        inverse_name='product_id'
    )

    @api.multi
    def copy(self, default=None):
        if not default:
            default = {}
        default['product_customer_code_ids'] = False
        return super(ProductProduct, self.with_context(copy=True))\
            .copy(default)

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=80):
        res = super(ProductProduct, self).name_search(
            cr, user, name, args, operator, context, limit)
        if not context:
            context = {}
        product_customer_code_obj = self.pool.get('product.customer.code')
        if not res:
            ids = []
            partner_id = context.get('partner_id', False)
            if partner_id:
                id_prod_code = \
                    product_customer_code_obj.search(cr, user,
                                                     [('product_code',
                                                       '=', name),
                                                      ('partner_id', '=',
                                                       partner_id)],
                                                     limit=limit,
                                                     context=context)
                # TODO: Search for product customer name
                id_prod = id_prod_code and product_customer_code_obj.browse(
                    cr, user, id_prod_code, context=context) or []
                for ppu in id_prod:
                    ids.append(ppu.product_id.id)
            if ids:
                res = self.name_get(cr, user, ids, context)
        return res
