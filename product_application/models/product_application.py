# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductApplication(models.Model):
    _name = 'product.application'

    name = fields.Char('Application Name', required=True)

    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_template_application_rel',
        column1='application_id',
        column2='product_tmpl_id',
        string='Product Templates',
    )
