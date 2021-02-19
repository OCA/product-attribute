# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = "product.category"

    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will allow you to hide the "
        "product category without removing it.",
    )

    @api.constrains("active")
    def _check_archive(self):
        to_archive = self.filtered(lambda r: not r.active)
        if (
            self.env["product.template"]
            .with_context(active_test=False)
            .search([("categ_id", "child_of", to_archive.ids)])
        ):
            raise ValidationError(
                _(
                    "At least one category that you are trying to archive or one "
                    "of its children has one or more product linked to it."
                )
            )
