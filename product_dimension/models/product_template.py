# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False,
    )
    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id):
        volume = 0
        if product_length and product_height and product_width and uom_id:
            length = self.convert_to_uom(product_length, uom_id)
            height = self.convert_to_uom(product_height, uom_id)
            width = self.convert_to_uom(product_width, uom_id)

            volume = length * height * width

        return volume

    @api.onchange(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
        )

    def convert_to_uom(self, measure, dimensional_uom):
        if self.env['ir.config_parameter'].sudo().get_param('product.volume_in_cubic_feet'):
            to_uom = self.env.ref('uom.product_uom_foot')
        else:
            to_uom = self.env.ref('uom.product_uom_meter')

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=to_uom,
            round=False,
        )
