# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    volume = fields.Float(
        help="The volume of the contents, not including any packaging, etc."
    )
    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume Unit of Measure",
        domain="[('measure_type', '=', 'volume')]",
        default=lambda x: x._get_volume_uom_id_from_ir_config_parameter(),
    )
    volume_uom_name = fields.Char(
        string="Volume unit of measure label",
        related="volume_uom_id.name",
        readonly=True,
    )

    weight = fields.Float(
        help="The weight of the contents, not including any packaging, etc."
    )

    weight_uom_id = fields.Many2one(
        "uom.uom",
        string="Weight Unit of Measure",
        domain="[('measure_type', '=', 'weight')]",
        compute=False,
        default=lambda x: x._get_weight_uom_id_from_ir_config_parameter(),
    )

    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="weight_uom_id.name",
        readonly=True,
    )

    @api.model
    def _get_volume_uom_id_from_ir_config_parameter(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        default_uom = get_param("product_default_volume_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(int(default_uom))
        else:
            # no super available in v12
            return self.env["uom.uom"].search(
                [("measure_type", "=", "volume"), ("uom_type", "=", "reference")],
                limit=1,
            )

    @api.model
    def _get_weight_uom_id_from_ir_config_parameter(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        default_uom = get_param("product_default_weight_uom_id")
        if default_uom:
            return self.env["uom.uom"].browse(int(default_uom))
        else:
            return super()._get_weight_uom_id_from_ir_config_parameter()
