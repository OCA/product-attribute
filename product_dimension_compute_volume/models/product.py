# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Product(models.Model):
    _inherit = "product.product"

    volume = fields.Float(compute="_compute_volume", store=True)

    @api.depends(
        "product_length",
        "product_height",
        "product_width",
        "dimensional_uom_id",
        "volume_uom_id",
    )
    def _compute_volume(self):
        product_template = self.env["product.template"]
        for product in self:
            product.volume = product_template._calc_volume(
                product.product_length,
                product.product_height,
                product.product_width,
                product.dimensional_uom_id,
                product.volume_uom_id,
            )
