# -*- coding: utf-8 -*-
# Copyright 2012 Vauxoo - http://www.vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCustomerCode(models.Model):
    _name = "product.customer.code"
    _description = "Add multiple product customer codes"

    _rec_name = 'product_code'

    product_code = fields.Char(
        string='Customer Product Code',
        required=True,
        help="This customer's product code will be used when searching into"
             "a request for quotation.",
    )

    product_name = fields.Char(
        string='Customer Product Name',
        help="This customer's product name will be used when searching into"
             "a request for quotation.",
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        index=True,
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False,
        default=lambda self: self.env['res.company']._company_default_get(),
    )

    _sql_constraints = [
        ('unique_code', 'unique(product_code,company_id,partner_id)',
         'Product customer code must be unique'),
    ]
