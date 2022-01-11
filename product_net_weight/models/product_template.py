# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    net_weight = fields.Float(
        string="Net Weight",
        related="product_variant_ids.net_weight",
        digits=dp.get_precision("Stock Weight"),
        help="Net Weight of the product, container excluded.",
        readonly=False,
    )

    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")
