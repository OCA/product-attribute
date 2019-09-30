# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    name = fields.Char(string='Release')  # TODO Rename on the view
    artist_ids = fields.Many2many('res.partner', string='Artist(s)')
