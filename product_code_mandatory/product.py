# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class product_code_mandatory_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    _columns = {
        'default_code':  fields.char('Reference', size=64, required=True),
    }

    _defaults ={
        'default_code': lambda *a: 'NEW',
    }
