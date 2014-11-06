# -*- coding: utf-8 -*-
from openerp.osv import orm, fields


class ProductTemplate(orm.Model):

    _inherit = "product.template"

    _columns = {
        'categ_id': fields.many2one('product.category',
                                    'Pricing/Primary Category',
                                    required=True,
                                    change_default=True,
                                    domain="[('type', '=', 'normal')]",
                                    help="Select category for the current "
                                         "product. The accounting and stock "
                                         "properties come from this category"),
        'categ_ids': fields.many2many('product.category',
                                      'product_categ_rel',
                                      'product_id',
                                      'categ_id',
                                      string='Product Categories',
                                      domain="[('type', '=', 'normal')]",
                                      help="Select additional categories "
                                           "for the current product")
        }
