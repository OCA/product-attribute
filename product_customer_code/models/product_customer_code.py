# coding: utf-8
# Copyright 2017 Vauxoo (https://www.vauxoo.com) info@vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import fields, models


class ProductCustomerCode(models.Model):

    _name = "product.customer.code"
    _description = "Add many Customer's Code"

    _rec_name = 'product_code'

    product_code = fields.Char('Customer Product Code', required=True,
                               help="This customer's product "
                               "code will be used when searching into a "
                               "request for quotation.")
    product_name = fields.Char('Customer Product Name', help="This customer's "
                               "product name will be used when searching into "
                               "a request for quotation.")
    product_id = fields.Many2one('product.product', 'Product', required=True,
                                 help='Product Identification')
    partner_id = fields.Many2one('res.partner', 'Customer', required=True,
                                 help='Partner Reference')
    company_id = fields.Many2one(
        'res.company', 'Company', default=lambda self:
        self.env['res.company']._company_default_get('product.customer.code'))

    def _auto_init(self, cr, context=None):
        res = super(ProductCustomerCode, self)._auto_init(cr, context=context)
        cr.execute(
            """SELECT indexname
            FROM pg_indexes
            WHERE indexname = 'product_customer_code_index' and
            tablename = 'product_customer_code'""")
        if not cr.fetchone():
            cr.execute(
                """CREATE INDEX product_customer_code_index
                ON product_customer_code (product_code, partner_id)""")
        return res

    _sql_constraints = [
        ('unique_code', 'unique(product_code,company_id,partner_id)',
         'Product Code of customer must be unique'),
    ]
