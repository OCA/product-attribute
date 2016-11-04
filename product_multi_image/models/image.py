# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from odoo import api, fields, models


class Image(models.Model):
    _inherit = "base_multi_image.image"

    product_variant_ids = fields.Many2many(
        comodel_name="product.product", string="Visible in these variants",
        help="If you leave it empty, all variants will show this image. "
             "Selecting one or several of the available variants, you "
             "restrict the availability of the image to those variants.")
    product_variant_count = fields.Integer(
        compute="_compute_product_variant_count")

    @api.multi
    def _compute_product_variant_count(self):
        for image in self:
            image.product_variant_count = len(image.product_variant_ids)
