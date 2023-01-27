# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    supplier_quantity = fields.Float(
        "Supplier Quantity",
        default=0.0,
        digits="Product Unit Of Measure",
        help="The quantity in stock at the supplier.",
    )
