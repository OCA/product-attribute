# -*- coding: utf-8 -*-
from odoo import models, fields, api, osv


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    type = fields.Selection(
        selection=[('customer', 'Customer'),
                   ('supplier', 'Supplier')],
        default='supplier')

    @api.multi
    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'supplier':
            return {'domain': {'name': [('supplier', '=', True)]}}
        elif self.type == 'customer':
            return {'domain': {'name': [('customer', '=', True)]}}
        return {'domain': {'name': []}}

    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Add search argument for field type if the context says so.
        """
        type_partner = self._context.get('supplierinfo_type', 'supplier')
        if not any(arg[0] == 'type' for arg in args):
            args = osv.expression.AND([args, [('type', '=', type_partner)]])
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count)
