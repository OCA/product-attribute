# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class UomUom(models.Model):

    _inherit = "uom.uom"

    _sql_constraints = [
        (
            "uom_qty_category_unique",
            "EXCLUDE (factor WITH =, category_id WITH =)" "WHERE (active=True)",
            "Only one active unit of measure per factor and per category should be active.",
        )
    ]
