# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductArtist(models.Model):

    _name = 'product.artist'
    _description = 'Artist'
    _order = 'name'

    name = fields.Char(required=True)
