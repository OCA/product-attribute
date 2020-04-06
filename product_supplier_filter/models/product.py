# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _name = "product.template"

    seller_id = fields.Many2one(
        related='seller_ids.name',
        domain=[('supplier', '=', True)],
    )
