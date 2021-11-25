# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductState(models.Model):

    _inherit = "product.state"

    deactivate_product = fields.Boolean(
        help="Check this if you want to archive product when reaching this state."
    )
    activate_product = fields.Boolean(
        help="Check this if you want to un-archive product when reaching this state."
    )

    @api.constrains("deactivate_product", "activate_product")
    def _check_product_inactive_active(self):
        if any(state.deactivate_product and state.activate_product for state in self):
            raise ValidationError(
                _(
                    "You cannot have both 'Deactivate Product' and "
                    "'Activate Product' options at the same time!"
                )
            )
