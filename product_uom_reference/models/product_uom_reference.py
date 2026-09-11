# Copyright 2025 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductUomReference(models.Model):
    _name = "product.uom.reference"
    _description = "Product UOM Reference"

    name = fields.Char(required=True, translate=True)
    uom_id = fields.Many2one("uom.uom", required=True)
    uom_reference_id = fields.Many2one("uom.uom", required=True)
    ratio = fields.Float(required=True)

    def _compute_display_name(self):
        for uom_reference in self:
            uom_reference.display_name = (
                f"{uom_reference.name} "
                f"[{uom_reference.uom_id.name}-"
                f"{uom_reference.uom_reference_id.name}]"
            )

    @api.constrains("uom_id", "uom_reference_id")
    def _check_uom_reference(self):
        for uom_reference in self:
            if uom_reference.uom_id == uom_reference.uom_reference_id:
                raise ValidationError(
                    self.env._(
                        "The unit of measurement and the reference "
                        "unit of measurement must be different."
                    )
                )
