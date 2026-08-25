# Copyright 2025 ACSONE SA/NV (<https://acsone.eu>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    from_default_level_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        related="product_variant_ids.from_default_level_packaging_id",
        string="Default packaging",
        help="This is the default packaging of this product coming "
        "from the default packaging level.",
    )
