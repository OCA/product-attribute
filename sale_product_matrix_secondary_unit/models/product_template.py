# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_template_matrix(self, **kwargs):
        matrix = super()._get_template_matrix(**kwargs)
        # The default secondary unit
        if self.sale_secondary_uom_id:
            matrix["secondary_unit_id"] = self.sale_secondary_uom_id.id
        # Optional secondary units
        if self.secondary_uom_ids:
            matrix["secondary_units"] = [
                {"name": f"{su.name} {su.factor} {su.sudo().uom_id.name}", "id": su.id}
                for su in self.secondary_uom_ids
            ]
        matrix["uom_name"] = self.uom_id.name
        return matrix
