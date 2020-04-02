# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductScaleGroup(models.Model):
    _name = 'product.scale.group'
    _description = 'Product Scale Group'

    # Compute Section
    def _compute_product_qty(self):
        for group in self:
            group.product_qty = len(group.product_ids)

    # Column Section
    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    external_identity = fields.Char('External ID', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        index=True,
        default=lambda self:
        self.env['res.company']._company_default_get('product.product')
    )
    scale_system_id = fields.Many2one(
        'product.scale.system',
        'Scale System',
        required=True
    )
    product_ids = fields.One2many(
        'product.product',
        'scale_group_id',
        'Products'
    )
    product_qty = fields.Integer(
        compute='_compute_product_qty',
        string='Products Quantity'
    )

    @api.multi
    def send_all_to_scale_create(self):
        for scale_group in self:
            scale_group.product_ids.send_scale_create()

    @api.multi
    def send_all_to_scale_write(self):
        for scale_group in self:
            scale_group.product_ids.send_scale_write()
