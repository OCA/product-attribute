# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_default_weight_uom_id = fields.Many2one(
        "uom.uom",
        "Default Weight Unit of Measure",
        config_parameter="product_default_weight_uom_id",
        help="Default unit of measure to express product weight",
        domain=lambda self: self.env["product.template"]._get_weight_uom_domain(),
    )
    product_default_volume_uom_id = fields.Many2one(
        "uom.uom",
        "Default Volume Unit of Measure",
        config_parameter="product_default_volume_uom_id",
        help="Default unit of measure to express product volume",
        domain=lambda self: self.env["product.template"]._get_volume_uom_domain(),
    )
    product_default_length_uom_id = fields.Many2one(
        "uom.uom",
        "Default Length Unit of Measure",
        config_parameter="product_default_length_uom_id",
        help="Default unit of measure to express product length",
        domain=lambda self: self.env["product.template"]._get_length_uom_domain(),
    )

    @api.constrains(
        "product_default_weight_uom_id",
        "product_default_volume_uom_id",
        "product_default_length_uom_id",
    )
    def _check_default_logistics_uom_compatibility(self):
        product_template = self.env["product.template"]
        for settings in self:
            for uom_type in ("weight", "volume", "length"):
                field_name = f"product_default_{uom_type}_uom_id"
                uom = settings[field_name]
                reference_uom = product_template._get_core_uom_reference(uom_type)
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
