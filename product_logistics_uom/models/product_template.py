# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_volume = fields.Float(
        "Volume in product UOM",
        compute="_compute_product_volume",
        inverse="_inverse_product_volume",
        digits="Volume",
    )
    product_weight = fields.Float(
        "Weight in product UOM",
        compute="_compute_product_weight",
        digits="Stock Weight",
        inverse="_inverse_product_weight",
        store=True,
    )

    # remove rounding from volume and weight
    # this is needed to avoid rounding errors when converting between units
    # and is safe since we display the volume and weight in the product's
    # volume and weight UOM. In the same time, we need to keep the volume
    # we ensure that no information is lost by storing the volume and weight
    # without rounding.
    volume = fields.Float(digits=False)
    weight = fields.Float(digits=False)
    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume Unit of Measure",
        default=lambda self: self._get_volume_uom_id_from_ir_config_parameter(),
        domain=lambda self: self._get_volume_uom_domain(),
    )
    volume_uom_name = fields.Char(
        string="Volume unit of measure label",
        related="volume_uom_id.name",
        compute=None,
    )
    weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Weight Unit of Measure",
        default=lambda self: self._get_weight_uom_id_from_ir_config_parameter(),
        domain=lambda self: self._get_weight_uom_domain(),
    )
    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="weight_uom_id.name",
        compute=None,
    )
    show_volume_uom_warning = fields.Boolean(
        help="Technical field used to warn the user to change the volume"
        "uom since the value for product_volume is too small and has been"
        "rounded.",
        compute="_compute_show_volume_uom_warning",
    )
    show_weight_uom_warning = fields.Boolean(
        help="Technical field used to warn the user to change the weight"
        "uom since the value for product_weight is too small and has been"
        "rounded.",
        compute="_compute_show_weight_uom_warning",
    )

    @api.model
    def _get_volume_uom_id_from_ir_config_parameter(self):
        uom_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_int("product_default_volume_uom_id")
        )
        if uom_id:
            uom = self.env["uom.uom"].browse(uom_id).exists()
            if uom:
                return uom
        return super()._get_volume_uom_id_from_ir_config_parameter()

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        uom_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_int("product_default_weight_uom_id")
        )
        if uom_id:
            uom = self.env["uom.uom"].browse(uom_id).exists()
            if uom:
                return uom
        return super()._get_weight_uom_id_from_ir_config_parameter()

    @api.model
    def _get_length_uom_id_from_ir_config_parameter(self):
        uom_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_int("product_default_length_uom_id")
        )
        if uom_id:
            uom = self.env["uom.uom"].browse(uom_id).exists()
            if uom:
                return uom
        return super()._get_length_uom_id_from_ir_config_parameter()

    @api.model
    def _get_core_uom_reference(self, uom_type):
        if uom_type == "weight":
            return super()._get_weight_uom_id_from_ir_config_parameter()
        if uom_type == "volume":
            return super()._get_volume_uom_id_from_ir_config_parameter()
        if uom_type == "length":
            return super()._get_length_uom_id_from_ir_config_parameter()
        raise ValueError(f"Unsupported unit type: {uom_type}")

    @api.model
    def _get_compatible_uom_domain(self, uom_type):
        reference_uom = self._get_core_uom_reference(uom_type)
        if not reference_uom:
            return [("id", "=", False)]
        compatible_uom_ids = []
        uoms = self.env["uom.uom"].search([], limit=1000)
        for uom in uoms:
            if uom == reference_uom or uom._has_common_reference(reference_uom):
                compatible_uom_ids.append(uom.id)
        return [("id", "in", compatible_uom_ids)]

    @api.model
    def _get_weight_uom_domain(self):
        return self._get_compatible_uom_domain("weight")

    @api.model
    def _get_volume_uom_domain(self):
        return self._get_compatible_uom_domain("volume")

    @api.model
    def _get_length_uom_domain(self):
        return self._get_compatible_uom_domain("length")

    @api.constrains("weight_uom_id", "volume_uom_id")
    def _check_logistics_uom_compatibility(self):
        for template in self:
            for uom_type in ("weight", "volume"):
                field_name = f"{uom_type}_uom_id"
                uom = template[field_name]
                reference_uom = template._get_core_uom_reference(uom_type)
                if (
                    uom
                    and reference_uom
                    and uom != reference_uom
                    and not uom._has_common_reference(reference_uom)
                ):
                    raise ValidationError(
                        self.env._(
                            "The selected unit must be compatible with %s.",
                            reference_uom.name,
                        )
                    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.product_volume",
        "volume",
        "volume_uom_id",
    )
    def _compute_product_volume(self):
        for template in self:
            template.product_volume = (
                template.product_variant_ids.product_volume
                if template.product_variant_count == 1
                else 0.0
            )

    def _inverse_product_volume(self):
        for template in self:
            if template.product_variant_count == 1:
                template.product_variant_ids.product_volume = template.product_volume

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.product_weight",
        "weight",
        "weight_uom_id",
    )
    def _compute_product_weight(self):
        for template in self:
            template.product_weight = (
                template.product_variant_ids.product_weight
                if template.product_variant_count == 1
                else 0.0
            )

    def _inverse_product_weight(self):
        for template in self:
            if template.product_variant_count == 1:
                template.product_variant_ids.product_weight = template.product_weight

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.show_volume_uom_warning",
        "volume",
        "volume_uom_id",
    )
    def _compute_show_volume_uom_warning(self):
        for template in self:
            template.show_volume_uom_warning = (
                template.product_variant_ids.show_volume_uom_warning
                if template.product_variant_count == 1
                else False
            )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.show_weight_uom_warning",
        "weight",
        "weight_uom_id",
    )
    def _compute_show_weight_uom_warning(self):
        for template in self:
            template.show_weight_uom_warning = (
                template.product_variant_ids.show_weight_uom_warning
                if template.product_variant_count == 1
                else False
            )
