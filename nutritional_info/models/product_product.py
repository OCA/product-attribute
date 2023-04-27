# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    nutritional_reference_qty = fields.Float(
        string="Nutritional reference quantity", default=100
    )
    nutritional_reference_uom = fields.Many2one(
        comodel_name="uom.uom",
        default=lambda x: x.env.ref("uom.product_uom_gram", raise_if_not_found=False),
    )
    nutritional_value_ids = fields.One2many(
        comodel_name="nutritional.value",
        inverse_name="product_id",
    )
