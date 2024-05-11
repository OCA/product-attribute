# Copyright 2023 Akretion (https://www.akretion.com).
# @author Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    level = fields.Integer(
        compute="_compute_level",
        store=True,
        recursive=True,
        help="The number of parents this category has",
    )

    @api.depends("parent_id", "parent_id.level")
    def _compute_level(self):
        for record in self:
            if record.parent_id:
                record.level = record.parent_id.level + 1
            else:
                record.level = 0
