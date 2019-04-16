# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    supplierinfo_type = fields.Selection(
        selection=[
            ('customer', 'Customer'),
            ('supplier', 'Supplier')],
        string='Type',
        oldname='type',
        default='supplier')

    @api.onchange('supplierinfo_type')
    def _onchange_type(self):
        if self.supplierinfo_type == 'supplier':
            return {'domain': {'name': [('supplier', '=', True)]}}
        elif self.supplierinfo_type == 'customer':
            return {'domain': {'name': [('customer', '=', True)]}}
        return {'domain': {'name': []}}

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        """Add search argument for field type if the context says so. This
        should be in old API because context argument is not the last one.
        """
        if not any(arg[0] == 'supplierinfo_type' for arg in args):
            args += [('supplierinfo_type', '=',
                      self.env.context.get('supplierinfo_type', 'supplier'))]
        return super(ProductSupplierinfo, self)._search(
            args, offset=offset, limit=limit, order=order, count=count,
            access_rights_uid=access_rights_uid)
