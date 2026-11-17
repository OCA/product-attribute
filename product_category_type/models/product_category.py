# Copyright 2021 Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    parent_id = fields.Many2one(domain="[('type', '=', 'view')]")

    type = fields.Selection(
        selection=[("view", "View"), ("normal", "Normal")],
        string="Category Type",
        default="normal",
        required=True,
        help="A category of the view type is a virtual category"
        " that can be used as the parent of another category"
        " to create a hierarchical structure.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        new_items = super().create(vals_list)
        # new created parent categories will be set to 'view' type
        # to avoid futur misconfiguration
        new_items.filtered(lambda x: x.child_id and x.type == "normal").write(
            {"type": "view"}
        )
        return new_items
