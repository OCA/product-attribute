# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    show_update_cost = fields.Boolean(compute="_compute_show_update_cost")

    def _compute_show_update_cost(self):
        """A user could have full cost permissions but no product edition permissions.
        We want to prevent those from updating costs."""
        for product in self:
            product.show_update_cost = self.check_access_rights(
                "write", raise_exception=False
            )
