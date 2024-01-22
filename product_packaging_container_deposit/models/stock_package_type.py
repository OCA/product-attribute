# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PackageType(models.Model):
    _inherit = "stock.package.type"

    container_deposit_product_id = fields.Many2one(
        "product.product", domain=[("type", "=", "service")]
    )
