# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    drained_weight = fields.Float(
        digits="Stock Weight",
        help="Drained Weight of the product, fluid excluded.",
    )

    @api.constrains("drained_weight", "net_weight")
    def _check_drained_weight(self):
        for product in self:
            if product.net_weight and product.drained_weight > product.net_weight:
                raise ValidationError(
                    _("The drained weight of product must be lower than net_weight.")
                )
