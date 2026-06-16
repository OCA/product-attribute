# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    product_life_period_id = fields.Many2one(
        "product.life.period", string="Life Period", index=True
    )
