# Copyright 2025 ACSONE SA/NV (<https://acsone.eu>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import api, fields, models
from odoo.fields import first


class ProductProduct(models.Model):
    _inherit = "product.product"

    from_default_level_packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        compute="_compute_from_default_level_packaging_id",
        string="Default packaging",
        help="This is the default packaging of this product coming "
        "from the default packaging level.",
    )

    @api.depends("packaging_ids.packaging_level_id.is_default")
    def _compute_from_default_level_packaging_id(self):
        for product in self:
            product.from_default_level_packaging_id = first(
                product.packaging_ids.filtered("packaging_level_id.is_default")
            )
