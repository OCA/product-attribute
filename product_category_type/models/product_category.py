# Copyright 2021 Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    parent_id = fields.Many2one(domain="[('type', '=', 'view')]")

    type = fields.Selection(
        selection=[("view", "View"), ("normal", "Normal")],
        string="Category Type",
        default="normal",
        help="A category of the view type is a virtual category"
        " that can be used as the parent of another category"
        " to create a hierarchical structure.",
    )
