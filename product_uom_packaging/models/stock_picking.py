# Copyright 2025 Bemade Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    package_incompatibility_warning = fields.Text(
        compute="_compute_package_incompatibility_warning",
        help="Aggregated warning messages for package incompatibilities in move lines.",
    )

    has_package_incompatibility = fields.Boolean(
        compute="_compute_package_incompatibility_warning",
        help="True when any move line has package incompatibility.",
    )

    @api.depends(
        "move_line_ids.is_package_incompatible",
        "move_line_ids.package_compatibility_warning",
    )
    def _compute_package_incompatibility_warning(self):
        """Aggregate package compatibility warnings from all move lines"""
        for picking in self:
            warnings = []
            for line in picking.move_line_ids:
                if line.is_package_incompatible and line.package_compatibility_warning:
                    product_name = line.product_id.display_name or "Unknown"
                    warnings.append(
                        f"• {product_name}: {line.package_compatibility_warning}"
                    )

            if warnings:
                picking.package_incompatibility_warning = "\n".join(warnings)
                picking.has_package_incompatibility = True
            else:
                picking.package_incompatibility_warning = False
                picking.has_package_incompatibility = False
