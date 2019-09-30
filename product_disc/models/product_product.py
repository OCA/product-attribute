# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    record_format = fields.Selection(
        [('vinyl', 'Vinyl'), ('cd', 'CD')],  # TODO add more formats
        string='Format',
    )
    country_id = fields.Many2one('res.country')
    release_year = fields.Char()  # Can't use Int because we need 'Unknown'
