# Copyright 2019, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductUom(models.Model):
    _inherit = "uom.uom"

    use_type = fields.Selection(
        [
            ("sale", "Unit available for sales"),
            ("purchase", "Unit available for purchases"),
            ("both", "Unit available for sales and purchases"),
        ],
        required=True,
        default="both",
    )
