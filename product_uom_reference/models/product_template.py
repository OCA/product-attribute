# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_reference_id = fields.Many2one(
        "product.uom.reference", domain="[('uom_id', '=', uom_id)]"
    )
