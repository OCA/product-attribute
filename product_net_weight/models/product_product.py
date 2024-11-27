# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class ProductProduct(models.Model):
    _inherit = "product.product"

    net_weight = fields.Float(
        digits="Stock Weight",
        help="Weight of the product without container nor packaging.",
    )

    # Explicit field, renaming it
    weight = fields.Float(
        string="Gross Weight",
        help="Weight of the product with its container and packaging.",
    )

    @api.constrains("net_weight", "weight")
    def _check_net_weight(self):
        prec = self.env["decimal.precision"].precision_get("Stock Weight")
        for product in self:
            if (
                not float_is_zero(product.weight, precision_digits=prec)
                and float_compare(
                    product.net_weight, product.weight, precision_digits=prec
                )
                > 0
            ):
                raise ValidationError(
                    _("The net weight of product '%s' must be lower than gross weight.")
                    % product.display_name
                )
