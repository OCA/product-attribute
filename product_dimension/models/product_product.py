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
        help="UoM for length, height, width",
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )

    @api.depends(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for product in self:
            product.volume = template_obj._calc_volume(
                product.product_length,
                product.product_height,
                product.product_width,
                product.dimensional_uom_id,
            )
