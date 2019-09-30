# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    label_ids = fields.Many2many('res.partner')
    country_id = fields.Many2one('res.country')
