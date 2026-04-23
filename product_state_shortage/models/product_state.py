# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductState(models.Model):
    _inherit = "product.state"

    is_shortage = fields.Boolean(
        string="Is Shortage State",
        help="If checked, products in this state will be processed by a "
        "cron to revert to default state if stock is available.",
    )

    @api.constrains("is_shortage", "default")
    def _check_shortage_not_default(self):
        for record in self:
            if record.is_shortage and record.default:
                raise ValidationError(
                    _(
                        "A product state cannot be both the 'Default' state and "
                        "a 'Shortage' state at the same time."
                    )
                )
