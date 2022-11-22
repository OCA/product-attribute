# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    net_weight = fields.Float(
        digits="Stock Weight",
        help="Net Weight of the product, container excluded.",
    )

    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")
