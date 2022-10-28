# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_standard_price_read_only = fields.Boolean(
        compute="_compute_is_standard_price_read_only",
        help="Indicates if the current user has read only access to standard_price field",
    )

    def _compute_is_standard_price_read_only(self):
        self.write(
            {
                "is_standard_price_read_only": not self.env.user.has_group(
                    "product_cost_read_only.group_product_cost_edit"
                )
            }
        )
