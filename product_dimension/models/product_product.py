# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_length = fields.Float("length")
    product_height = fields.Float("height")
    product_width = fields.Float("width")
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        domain=lambda self: self._get_dimension_uom_domain(),
        help="UoM for length, height, width",
        default=lambda self: self.env.ref("uom.product_uom_meter"),
    )

    @api.onchange(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def onchange_calculate_volume(self):
        self.volume = self.env["product.template"]._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
        )

    @api.model
    def _get_dimension_uom_domain(self):
        return [("category_id", "=", self.env.ref("uom.uom_categ_length").id)]
