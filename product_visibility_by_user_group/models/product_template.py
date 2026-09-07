# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    visibility_group_ids = fields.Many2many(
        comodel_name="res.groups",
        relation="product_template_visibility_group_rel",
        column1="product_tmpl_id",
        column2="group_id",
        string="Visibility Groups",
        help=(
            "Leave empty to make the product visible to every user. "
            "Set groups to restrict product visibility to matching users."
        ),
    )
