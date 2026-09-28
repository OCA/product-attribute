# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]

    # image, image_medium, image_small fields are not available since 13.0

    image_1920 = fields.Binary(
        compute="_compute_image_1920",
        inverse="_inverse_image_1920",
        store=True,
    )

    @api.depends(
        "image_ids",
    )
    def _compute_image_1920(self):
        for product in self:
            if not product.image_ids:
                product.image_1920 = False
                continue
            else:
                images = product.image_ids.filtered(
                    lambda x, p=product: (
                        not x.product_variant_ids or p.product_variant_count == 1
                    )
                )
                if images:
                    product.image_1920 = (
                        images[0].with_context(bin_size=False).image_1920
                    )
                else:
                    product.image_1920 = (
                        product.image_ids[0].with_context(bin_size=False).image_1920
                    )

    def _inverse_image_1920(self):
        for product in self:
            images = product.image_ids.filtered(
                lambda x, p=product: (
                    not x.product_variant_ids or p.product_variant_count == 1
                )
            )
            img_new = product.with_context(bin_size=False).image_1920
            if images:
                if images[0].attachment_image != img_new:
                    images[0].attachment_image = img_new
            else:
                if img_new:
                    product.image_ids = [
                        (
                            0,
                            False,
                            {
                                "name": product.name,
                                "attachment_image": img_new,
                                "owner_id": product.id,
                                "owner_model": "product.template",
                            },
                        )
                    ]
