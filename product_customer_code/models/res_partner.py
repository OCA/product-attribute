# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_code_ids = fields.One2many(
        comodel_name='product.customer.code',
        inverse_name='partner_id',
        string='Products',
    )
