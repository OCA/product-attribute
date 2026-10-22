# Copyright 2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_variant_barcode_required = fields.Boolean(
        related="company_id.product_variant_barcode_required",
        readonly=False,
        groups="product.group_product_variant",
    )
