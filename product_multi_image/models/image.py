# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).
# © 2009 Sharoon Thomas Open Labs Business Solutions
# © 2014 Serv. Tecnol. Avanzados Pedro M. Baeza
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# © 2016 Pedro M. Baeza, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


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
