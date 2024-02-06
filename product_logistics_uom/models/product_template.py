# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_vol").id)
        ],
        default=lambda self: self._get_volume_uom_id_from_ir_config_parameter(),
    )
    volume_uom_name = fields.Char(
        string="Volume unit of measure label",
        related="volume_uom_id.name",
        readonly=True,
    )

    weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Weight Unit of Measure",
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_kgm").id)
        ],
        compute=False,
        default=lambda self: self._get_weight_uom_id_from_ir_config_parameter(),
    )

    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="weight_uom_id.name",
        readonly=True,
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
        get_param = self.env["ir.config_parameter"].sudo().get_param
        default_uom = get_param("product_default_volume_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(int(default_uom))
        else:
            return super()._get_volume_uom_id_from_ir_config_parameter()

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        default_uom = get_param("product_default_weight_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(int(default_uom))
        else:
            return super()._get_weight_uom_id_from_ir_config_parameter()

    @api.model
    def _get_length_uom_id_from_ir_config_parameter(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        default_uom = get_param("product_default_length_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(int(default_uom))
        else:
            return super()._get_length_uom_id_from_ir_config_parameter()

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.product_volume",
        "volume",
        "volume_uom_id",
    )
    def _compute_product_volume(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.product_volume = template.product_variant_ids.product_volume
        for template in self - unique_variants:
            template.product_volume = 0.0

    def _inverse_product_volume(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.product_volume = template.product_volume

    @api.depends("weight", "weight_uom_id")
    def _compute_product_weight(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.product_weight = template.product_variant_ids.product_weight
        for template in self - unique_variants:
            template.product_weight = 0.0

    def _inverse_product_weight(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.product_weight = template.product_weight

    @api.depends("volume", "volume_uom_id")
    def _compute_show_volume_uom_warning(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.show_volume_uom_warning = (
                template.product_variant_ids.show_volume_uom_warning
            )
        for template in self - unique_variants:
            template.show_volume_uom_warning = False

    @api.depends("weight", "weight_uom_id")
    def _compute_show_weight_uom_warning(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.show_weight_uom_warning = (
                template.product_variant_ids.show_weight_uom_warning
            )
        for template in self - unique_variants:
            template.show_weight_uom_warning = False

    def _prepare_variant_values(self, combination):
        res = super()._prepare_variant_values(combination)
        if self.product_volume:
            res.update(
                {
                    "product_volume": self.product_volume,
                }
            )
        if self.product_weight:
            res.update(
                {
                    "product_weight": self.product_weight,
                }
            )
        return res
