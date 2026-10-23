# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    stock_availability = fields.Selection(
        selection=[
            ("available", "Available"),
            ("limited", "Limited"),
            ("unavailable", "Unavailable"),
        ],
        help="This is the stock availability of this product for the supplier. "
        "If this is not managed, don't fill it in.",
    )
    stock_availability_readonly = fields.Boolean(
        compute="_compute_stock_availability_readonly",
    )

    def _compute_stock_availability_readonly(self):
        readonly = not self.env.user.has_group(
            "product_supplierinfo_stock_availability.group_supplierinfo_stock_availability"
        )
        self.stock_availability_readonly = readonly
