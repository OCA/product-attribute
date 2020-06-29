# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    application_ids = fields.One2many(
        string='Applications',
        comodel_name='product.application',
        inverse_name='product_tmpl_id'
    )
