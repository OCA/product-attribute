# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    is_shortage = fields.Boolean(
        string="Is Shortage State",
        help="If checked, products in this state will automatically revert to the "
        "default state when a stock receipt is validated.",
    )
