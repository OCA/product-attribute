# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class Product(models.Model):
    _inherit = 'product.product'

    additional_tax_ids = fields.Many2many(
        comodel_name='account.tax',
        string="Additional Taxes",
        domain=[('type_tax_use', '=', 'sale')],
    )
