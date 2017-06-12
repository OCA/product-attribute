# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
