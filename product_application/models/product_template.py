# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    application_ids = fields.Many2many(
        comodel_name='product.application',
        relation='product_template_application_rel',
        column1='product_tmpl_id',
        column2='application_id',
        string='Applications',
    )
