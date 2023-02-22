from odoo import api, fields, models

from ..constants import constants


##########################################
# Dimensions Mixin
##########################################
class DimensionsMixin(models.AbstractModel):
    _name = "ooops.dimensions.mixin"
    _description = "Dimensions Implementation for different Models"

    product_length = fields.Float(string="Length, mm", default=0.00)
    product_width = fields.Float(string="Width, mm", default=0.00)
    product_height = fields.Float(string="Height, mm", default=0.00)
    product_area_wh = fields.Float(
        string="Area, m2", digits=(10, 3), compute="_compute_dimensions", store=True
    )
    product_volume = fields.Float(
        string="Volume, m3", digits=(8, 4), compute="_compute_dimensions", store=True
    )
    product_perimeter = fields.Float(
        string="Perimeter, mm",
        help="Shape perimeter value storage",
    )

    # -- Compute square/cubic figure
    @api.depends("product_length", "product_width", "product_height")
    def _compute_dimensions(self):
        for rec in self:
            product_area_wh = rec.product_height * rec.product_width / 1000000
            rec.update(
                {
                    constants.PRODUCT_AREA_WH: product_area_wh,
                }
            )
