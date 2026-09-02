# Copyright 2019-2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"
    # Keep dimensional field names aligned with ``stock.package.type``
    # and ``delivery.carrier`` integrations while storing them on product packagings.

    height = fields.Float(help="Packaging Height")
    width = fields.Float(help="Packaging Width")
    packaging_length = fields.Float(string="Length", help="Packaging Length")

    length_uom_name = fields.Char(
        string="Length unit of measure label",
        compute="_compute_length_uom_name",
    )
    # OVERRIDE: to force NUMERIC with unlimited precision,
    # as for `uom.uom.relative_factor`, to support very small ratios
    volume = fields.Float(digits=0)

    _positive_height = models.Constraint(
        "CHECK(height>=0)",
        "Height must be positive",
    )
    _positive_width = models.Constraint(
        "CHECK(width>=0)",
        "Width must be positive",
    )
    _positive_length = models.Constraint(
        "CHECK(packaging_length>=0)",
        "Length must be positive",
    )

    def _compute_length_uom_name(self):
        """Show the configured length UoM next to dimensional fields."""
        product_template = self.env["product.template"]
        length_uom_name = (
            product_template._get_length_uom_name_from_ir_config_parameter()
        )
        for packaging in self:
            packaging.length_uom_name = length_uom_name

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # OVERRIDE to add the configured length UoM to list view field labels.
        res = super().fields_get(allfields, attributes)
        if self.env.context.get("uom_inline_field_labels"):
            ProductTemplate = self.env["product.template"]
            length_uom_name = (
                ProductTemplate._get_length_uom_name_from_ir_config_parameter()
            )
            for field_name in ("packaging_length", "width", "height"):
                if field_name in res and "string" in res[field_name]:
                    res[field_name]["string"] += f" ({length_uom_name})"
        return res

    @api.depends(
        "product_id.uom_id",
        "uom_id.factor",
        "packaging_length",
        "width",
        "height",
    )
    def _compute_volume(self):
        # OVERRIDE to compute packaging volume from dimensions when available.
        length_uom_id, volume_uom_id = self._get_configured_dimension_uoms()
        res = None
        if empty_dimension_packagings := self.filtered(
            lambda packaging: packaging._has_no_dimensions(length_uom_id)
        ):
            # If all dimensions are zero, fall back to the base product packaging
            # volume.
            res = super(ProductPackaging, empty_dimension_packagings)._compute_volume()
        complete_dimension_packagings = (self - empty_dimension_packagings).filtered(
            lambda packaging: packaging._has_all_dimensions(length_uom_id)
        )
        # Partial dimensions mean the user started entering package dimensions,
        # but the box is incomplete, so keep the historical zero result.
        partial_dimension_packagings = (
            self - empty_dimension_packagings - complete_dimension_packagings
        )
        partial_dimension_packagings.volume = 0
        # Complete dimensions mean the user entered a full box, so calculate
        # the volume.
        for packaging in complete_dimension_packagings:
            packaging.volume = packaging._calculate_volume(
                packaging.packaging_length,
                packaging.height,
                packaging.width,
                length_uom_id,
                volume_uom_id,
            )
        return res

    def _get_configured_dimension_uoms(self):
        """Return the configured length and volume UoMs."""
        product_template = self.env["product.template"]
        return (
            product_template._get_length_uom_id_from_ir_config_parameter(),
            product_template._get_volume_uom_id_from_ir_config_parameter(),
        )

    def _has_no_dimensions(self, length_uom_id):
        """Return whether all dimensions are zero in length UoM."""
        self.ensure_one()
        return all(
            length_uom_id.is_zero(measure) for measure in self._get_dimension_values()
        )

    def _has_all_dimensions(self, length_uom_id):
        """Return whether all dimensions are non-zero in length UoM."""
        self.ensure_one()
        return all(
            not length_uom_id.is_zero(measure)
            for measure in self._get_dimension_values()
        )

    def _get_dimension_values(self):
        """Return length, height, and width values as a tuple."""
        self.ensure_one()
        return (self.packaging_length, self.height, self.width)

    def _calculate_volume(
        self,
        packaging_length,
        height,
        width,
        length_uom_id,
        volume_uom_id,
    ):
        """Calculate dimensional packaging volume in the configured volume UoM."""
        length_m = self.convert_to_meters(packaging_length, length_uom_id)
        height_m = self.convert_to_meters(height, length_uom_id)
        width_m = self.convert_to_meters(width, length_uom_id)
        volume_m3 = length_m * height_m * width_m
        volume_in_volume_uom = self.convert_to_volume_uom(volume_m3, volume_uom_id)
        return volume_uom_id.round(volume_in_volume_uom)

    def convert_to_meters(self, measure, length_uom_id):
        """Convert a length value from the configured length UoM to meters."""
        uom_meters = self.env.ref("uom.product_uom_meter")
        return length_uom_id._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    def convert_to_volume_uom(self, measure, volume_uom_id):
        """Convert a cubic meter value to the configured volume UoM."""
        uom_m3 = self.env.ref("uom.product_uom_cubic_meter")
        return uom_m3._compute_quantity(
            qty=measure,
            to_unit=volume_uom_id,
            round=False,
        )
