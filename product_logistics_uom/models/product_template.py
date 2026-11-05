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
        default=lambda self: self._get_volume_uom_id_from_ir_config_parameter(),
    )
    volume_uom_name = fields.Char(
        string="Volume unit of measure label",
        compute=None,
        related="volume_uom_id.name",
    )

    weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Weight Unit of Measure",
        default=lambda self: self._get_weight_uom_id_from_ir_config_parameter(),
    )

    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        compute=None,
        related="weight_uom_id.name",
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
        get_int = self.env["ir.config_parameter"].sudo().get_int
        default_uom = get_int("product_default_volume_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(default_uom)
        return super()._get_volume_uom_id_from_ir_config_parameter()

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        get_int = self.env["ir.config_parameter"].sudo().get_int
        default_uom = get_int("product_default_weight_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(default_uom)
        return super()._get_weight_uom_id_from_ir_config_parameter()

    @api.model
    def _get_length_uom_id_from_ir_config_parameter(self):
        get_int = self.env["ir.config_parameter"].sudo().get_int
        default_uom = get_int("product_default_length_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(default_uom)
        return super()._get_length_uom_id_from_ir_config_parameter()

    # The variants do not exist yet when the inverses run during the template's
    # creation: like the standard volume and weight, the values in the product's UoM
    # are written again once the variants are created.
    def _get_related_fields_variant_template(self):
        return super()._get_related_fields_variant_template() + [
            "product_volume",
            "product_weight",
        ]

    # Since 20.0, the standard volume and weight of a template are shown and editable
    # on templates with several variants: they hold the value the variants share, and
    # writing them updates every variant. The values in the product's UoM follow the
    # same rule. They are read from the variants rather than from the template's own
    # volume and weight, which other modules may compute differently (e.g. the volume
    # from the dimensions in product_dimension).
    def _get_shared_variant_value(self, fname, default):
        self.ensure_one()
        values = set(self.product_variant_ids.mapped(fname))
        return values.pop() if len(values) == 1 else default

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.volume",
        "volume",
        "volume_uom_id",
    )
    def _compute_product_volume(self):
        for template in self:
            template.product_volume = template._get_shared_variant_value(
                "product_volume", 0.0
            )

    def _inverse_product_volume(self):
        for template in self:
            template.product_variant_ids.product_volume = template.product_volume

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.weight",
        "weight",
        "weight_uom_id",
    )
    def _compute_product_weight(self):
        for template in self:
            template.product_weight = template._get_shared_variant_value(
                "product_weight", 0.0
            )

    def _inverse_product_weight(self):
        for template in self:
            template.product_variant_ids.product_weight = template.product_weight

    @api.depends("product_variant_ids.volume", "volume", "volume_uom_id")
    def _compute_show_volume_uom_warning(self):
        for template in self:
            template.show_volume_uom_warning = template._get_shared_variant_value(
                "show_volume_uom_warning", False
            )

    @api.depends("product_variant_ids.weight", "weight", "weight_uom_id")
    def _compute_show_weight_uom_warning(self):
        for template in self:
            template.show_weight_uom_warning = template._get_shared_variant_value(
                "show_weight_uom_warning", False
            )
