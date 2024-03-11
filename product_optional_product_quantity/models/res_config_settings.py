# Copyright 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_product_optional_quantity = fields.Boolean(
        string="Optional Products Quantity",
        implied_group="product_optional_product_quantity.group_product_optional_quantity",
    )
