# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    customer_ids = fields.One2many(
        comodel_name='product.supplierinfo', inverse_name='product_tmpl_id',
        string='Customer', domain=[('supplierinfo_type', '=', 'customer')])
    supplier_ids = fields.One2many(
        comodel_name='product.supplierinfo', inverse_name='product_tmpl_id',
        string='Supplier', domain=[('supplierinfo_type', '=', 'supplier')])
    variant_supplier_ids = fields.One2many(
        comodel_name='product.supplierinfo', inverse_name='product_tmpl_id',
        string='Supplier', domain=[('supplierinfo_type', '=', 'supplier')])
