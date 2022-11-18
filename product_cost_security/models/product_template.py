# Copyright 2018 Sergio Teruel - Tecnativa <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(groups="product_cost_security.group_product_cost")
    user_can_update_cost = fields.Boolean(compute="_compute_user_can_update_cost")

    @api.depends_context("uid")
    def _compute_user_can_update_cost(self):
        """A user could have full cost permissions but no product edition permissions.
        We want to prevent those from updating costs."""
        for product in self:
            product.user_can_update_cost = self.env.user.has_group(
                "product_cost_security.group_product_edit_cost"
            )
