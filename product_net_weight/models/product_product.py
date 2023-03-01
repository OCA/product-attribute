# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    net_weight = fields.Float(
        digits="Stock Weight",
        help="Net Weight of the product, container excluded.",
    )

    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")

    @api.constrains("net_weight", "weight")
    def _check_net_weight(self):
        for product in self:
            if product.weight and product.net_weight > product.weight:
                raise ValidationError(
                    _("The net weight of product must be lower than gross weight.")
                )
