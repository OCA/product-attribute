# Copyright 2020 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_default_weight_uom_id = fields.Many2one(
        "uom.uom",
        "Default Weight Unit of Measure",
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_kgm").id)
        ],
        config_parameter="product_default_weight_uom_id",
        help="Default unit of measure to express product weight",
    )

    product_default_volume_uom_id = fields.Many2one(
        "uom.uom",
        "Default Volume Unit of Measure",
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.product_uom_categ_vol").id)
        ],
        config_parameter="product_default_volume_uom_id",
        help="Default unit of measure to express product volume",
    )

    product_default_length_uom_id = fields.Many2one(
        "uom.uom",
        "Default Length Unit of Measure",
        domain=lambda self: [
            ("category_id", "=", self.env.ref("uom.uom_categ_length").id)
        ],
        config_parameter="product_default_length_uom_id",
        help="Default unit of measure to express product length",
    )
