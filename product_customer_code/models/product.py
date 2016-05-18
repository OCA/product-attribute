# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class product_product(orm.Model):
    _inherit = "product.product"

    _columns = {
        'product_customer_code_ids': fields.one2many('product.customer.code',
                                                     'product_id',
                                                     'Customer Codes'),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default['product_customer_code_ids'] = False
        res = super(product_product, self).copy(
            cr, uid, id, default=default, context=context)
        return res

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                    context=None, limit=80):
        res = super(product_product, self).name_search(
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
