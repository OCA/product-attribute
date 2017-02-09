# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools.translate import _


class product_code_unique_product(osv.osv):
    _name = "product.product"
    _inherit = "product.product"

    def _check_defaultcode_and_variants(self, cr, uid, ids):
        for product in self.browse(cr, uid, ids):
            res = self.search(cr, uid, [('default_code', '=', product.default_code),
                                         ('variants', '=', product.variants)
                                       ])
            # Result may contain the current product if it's active: we remove it here.
            if product.id in res:
                res.remove(product.id)
            if len(res):
                # If we have any results left
                # we have duplicate entries
                return False
        return True

    _constraints = [(_check_defaultcode_and_variants,
                    _('Reference/Variant has to be unique.'),
                    ['default_code', 'variants'])
                   ]

    _sql_constraints = [('default_code_uniq', 'unique (default_code, variants)', """Reference/Variant has to be unique."""),]

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}

        if not default:
            default = {}
        if 'default_code' not in default:
            default = default.copy()
            product = self.read(cr, uid, id, ['default_code'], context=context)
            default['default_code'] = product['default_code'] + _(' (copy)')

        return super(product_code_unique_product, self).copy(cr=cr, uid=uid, id=id, default=default, context=context)
