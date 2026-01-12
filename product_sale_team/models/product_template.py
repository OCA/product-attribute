# Copyright (C) 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sales_team_id = fields.Many2one(
        comodel_name="crm.team",
        help="Default sales team responsible for this product.",
    )
