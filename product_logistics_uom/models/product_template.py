# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    volume_uom_id = fields.Many2one(
        "uom.uom",
        string="Volume Unit of Measure",
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_vol").id)
        ],
        default=lambda x: x._get_volume_uom_id_from_ir_config_parameter(),
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
        default=lambda x: x._get_weight_uom_id_from_ir_config_parameter(),
    )

    weight_uom_name = fields.Char(
        string="Weight unit of measure label",
        related="weight_uom_id.name",
        readonly=True,
    )

    product_uom_readonly = fields.Boolean(compute="_compute_product_uom_readonly")

    def _compute_product_uom_readonly(self):
        # helper for view form
        self.product_uom_readonly = not self.env.user.has_group("uom.group_uom")

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
