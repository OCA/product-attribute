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
from openerp import models, fields


class ProductCustomerCode(models.Model):
    _name = "product.customer.code"
    _description = "Add manies Code of Customer's"

    product_name = fields.Char(string='Customer Product Name',
                               help="""This customer's product name will
                                        be used when searching into a
                                        request for quotation.""")
    product_code = fields.Char(string='Customer Product Code',
                               help="""This customer's product code
                                        will be used when searching into
                                        a request for quotation.""")
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer',
                                 required=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=False,
        default=lambda self: self.env['res.company']._company_default_get(
            'product.customer.code'))
