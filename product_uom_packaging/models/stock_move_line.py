# Copyright 2025 Bemade Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    package_type_id = fields.Many2one(
        "stock.package.type",
        help="Package type for this stock move line.",
    )

    package_compatibility_warning = fields.Text(
        compute="_compute_package_compatibility",
        help="Warning message when product doesn't fit in package type.",
    )

    is_package_incompatible = fields.Boolean(
        string="Package Incompatible",
        compute="_compute_package_compatibility",
        help="True when package type is incompatible with product.",
    )

    @api.depends("package_type_id", "product_id", "quantity", "product_uom_id")
    def _compute_package_compatibility(self):
        """Compute package compatibility warnings based on weight and volume
        constraints"""
        for line in self:
            line.package_compatibility_warning = False
            line.is_package_incompatible = False

            if not line.package_type_id or not line.product_id:
                continue

            # Check weight compatibility
            if line.package_type_id.max_weight > 0:
                total_weight = line.product_id.weight * line.quantity
                if total_weight > line.package_type_id.max_weight:
                    max_w = line.package_type_id.max_weight
                    line.package_compatibility_warning = (
                        f"Weight incompatibility: Product weight"
                        f" ({total_weight:.1f} kg) exceeds"
                        f" package max weight ({max_w:.1f} kg)"
                    )
                    line.is_package_incompatible = True
                    continue

            # Check volume compatibility (if package has dimensions)
            if (
                line.package_type_id.height > 0
                and line.package_type_id.width > 0
                and line.package_type_id.packaging_length > 0
            ):
                # Simple volume check - this is a basic implementation
                # In practice, you might want more sophisticated volume calculations
                package_volume = (
                    line.package_type_id.height
                    * line.package_type_id.width
                    * line.package_type_id.packaging_length
                )

                # For now, just warn if product has volume info that seems incompatible
                # This could be enhanced with actual product volume calculations
                if hasattr(line.product_id, "volume") and line.product_id.volume > 0:
                    if line.product_id.volume > package_volume:
                        line.package_compatibility_warning = (
                            f"Volume incompatibility: Product volume "
                            f"({line.product_id.volume:.1f}) "
                            f"exceeds package volume ({package_volume:.1f})"
                        )
                        line.is_package_incompatible = True
