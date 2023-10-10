# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import fields, models


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    packaging_level_id = fields.Many2one(
        "product.packaging.level",
        default=lambda self: self.env["product.packaging"].default_packaging_level_id(),
    )
