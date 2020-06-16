# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductApplication(models.Model):
    _name = 'product.application'

    name = fields.Char('Application Name', required=True)

    product_tmpl_id = fields.Many2one(
        'product.template',
        'Product Template',
        help="Product Template",
        required=False
    )
