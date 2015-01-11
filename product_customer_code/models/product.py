# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: Rodo (rodo@vauxoo.com),Moy (moylop260@vauxoo.com)
############################################################################
#    Migrated to Odoo 8.0 by Acysos S.L. - http://www.acysos.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_customer_code_ids = fields.One2many(
        comodel_name='product.customer.code', inverse_name='product_id',
        string='Customer Codes')

    @api.model
    def copy(self, default):
        if not default:
            default = {}
        default['product_customer_code_ids'] = False
        res = super(ProductTemplate, self).copy(default)
        return res

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        res = super(ProductTemplate, self).search(cr, uid, args, offset=offset,
                                                  limit=limit, order=order,
                                                  count=count)
        operator = False
        term = False
        for arg in args:
            if arg[0] == 'name':
                operator = arg[1]
                term = arg[2]
        if not res and operator is not False and term is not False:
            product_customer_code_obj = self.pool.get('product.customer.code')
            product_ids = set(product_customer_code_obj.search(
                cr, uid, [('product_code', operator, term)], limit=limit,
                context=context))
            if not limit or len(product_ids) < limit:
                limit2 = (limit - len(product_ids)) if limit else False
                product_ids.update(product_customer_code_obj.search(
                    cr, uid, [('product_name', operator, term)], limit=limit2,
                    context=context))
            product_ids = list(product_ids)

            product_datas = product_customer_code_obj.browse(cr, uid,
                                                             product_ids,
                                                             context)

            prod_ids = []
            for product_data in product_datas:
                prod_ids.append(product_data.product_id.id)
            res = prod_ids

        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        res = super(ProductProduct, self).search(cr, uid, args, offset=offset,
                                                 limit=limit, order=order,
                                                 context=context, count=count)
        operator = False
        term = False
        for arg in args:
            if arg[0] == 'name':
                operator = arg[1]
                term = arg[2]

        if not res and operator is not False and term is not False:
            cust_data_obj = self.pool.get('product.customer.code')
            cust_ids = set(cust_data_obj.search(
                cr, uid, [('product_code', operator, term)], limit=limit,
                context=context))
            if not limit or len(cust_ids) < limit:
                limit2 = (limit - len(cust_ids)) if limit else False
                cust_ids.update(cust_data_obj.search(
                    cr, uid, [('product_name', operator, term)], limit=limit2,
                    context=context))
            cust_ids = list(cust_ids)

            products_template = cust_data_obj.read(cr, uid, cust_ids,
                                                   ['product_id'], context)
            product_obj = self.pool.get('product.product')
            for template in products_template:
                prod_ids = product_obj.search(
                    cr, uid, [('product_tmpl_id', '=',
                               template['product_id'][0])], context=context)
                for prod_id in prod_ids:
                    res.append(prod_id)
        return res
