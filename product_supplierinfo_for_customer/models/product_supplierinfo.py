# -*- coding: utf-8 -*-
# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    type = fields.Selection(
        selection=[('customer', 'Customer'),
                   ('supplier', 'Supplier')], string='Type',
        default='supplier')

    @api.multi
    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'supplier':
            return {'domain': {'name': [('supplier', '=', True)]}}
        elif self.type == 'customer':
            return {'domain': {'name': [('customer', '=', True)]}}
        return {'domain': {'name': []}}

    def search(self, cr, uid, args, offset=0, limit=None, order=None,
               context=None, count=False):
        """Add search argument for field type if the context says so. This
        should be in old API because context argument is not the last one.
        """
        if context is None:
            context = {}
        if not any(arg[0] == 'type' for arg in args):
            args += [('type', '=',
                      context.get('supplierinfo_type', 'supplier'))]
        return super(ProductSupplierinfo, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)
