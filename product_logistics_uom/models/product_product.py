# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models
from odoo.tools import float_is_zero


class ProductProduct(models.Model):
    _inherit = "product.product"

    # remove rounding from volume and weight
    # this is needed to avoid rounding errors when converting between units
    # and is safe since we display the volume and weight in the product's
    # volume and weight UOM. In the same time, we need to keep the volume
    # we ensure that no information is lost by storing the volume and weight
    # without rounding.
    volume = fields.Float(digits=False)
    weight = fields.Float(digits=False)

    product_volume = fields.Float(
        "Volume in product UOM",
        digits="Volume",
        help="The volume in the product's volume UOM.",
        compute="_compute_product_volume",
        inverse="_inverse_product_volume",
    )
    product_weight = fields.Float(
        "Weight in product UOM",
        digits="Stock Weight",
        help="The weight in the product's weight UOM.",
        compute="_compute_product_weight",
        inverse="_inverse_product_weight",
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

    @api.depends("product_volume", "product_tmpl_id.volume_uom_id")
    def _compute_product_volume(self):
        odoo_volume_uom = (
            self.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.product_volume = odoo_volume_uom._compute_quantity(
                qty=product.volume,
                to_unit=product.volume_uom_id,
                round=False,  # avoid losing information
            )

    def _inverse_product_volume(self):
        odoo_volume_uom = (
            self.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.volume = product.volume_uom_id._compute_quantity(
                qty=product.product_volume,
                to_unit=odoo_volume_uom,
                round=False,  # avoid losing information
            )

    @api.depends("product_weight", "product_tmpl_id.weight_uom_id")
    def _compute_product_weight(self):
        odoo_weight_uom = (
            self.product_tmpl_id._get_weight_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.product_weight = odoo_weight_uom._compute_quantity(
                qty=product.weight,
                to_unit=product.weight_uom_id,
                round=False,  # avoid losing information
            )

    def _inverse_product_weight(self):
        odoo_weight_uom = (
            self.product_tmpl_id._get_weight_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.weight = product.weight_uom_id._compute_quantity(
                qty=product.product_weight, to_unit=odoo_weight_uom, round=False
            )

    @api.depends("product_volume", "product_tmpl_id.volume_uom_id", "volume")
    def _compute_show_volume_uom_warning(self):
        odoo_volume_uom = (
            self.product_tmpl_id._get_volume_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.show_volume_uom_warning = (
                float_is_zero(
                    product.product_volume, precision_rounding=odoo_volume_uom.rounding
                )
                and product.volume != 0.0
            )

    @api.depends("product_weight", "product_tmpl_id.weight_uom_id", "weight")
    def _compute_show_weight_uom_warning(self):
        odoo_weight_uom = (
            self.product_tmpl_id._get_weight_uom_id_from_ir_config_parameter()
        )
        for product in self:
            product.show_weight_uom_warning = (
                float_is_zero(
                    product.product_weight, precision_rounding=odoo_weight_uom.rounding
                )
                and product.weight != 0.0
            )
