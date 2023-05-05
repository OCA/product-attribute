# Copyright 2023 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    specific_supplierinfo_group_ids = fields.One2many(
        "product.supplierinfo.group",
        "product_id",
        name="Specific Supplier",
        help="This supplier group only apply to the current variante",
    )
