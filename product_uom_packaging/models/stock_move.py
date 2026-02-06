# Copyright 2025 Bemade Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    package_type_id = fields.Many2one(
        "stock.package.type",
        string="Intended Package Type",
        help="Package type intended for this stock move (for planning and guidance).",
    )
