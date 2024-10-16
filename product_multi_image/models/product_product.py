# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = [_name, "base_multi_image.owner"]

    # Make this field computed for getting only the available images
    image_ids = fields.One2many(
        comodel_name="base_multi_image.image",
        compute="_compute_image_ids",
        inverse="_inverse_image_ids",
    )

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.image_ids",
        "product_tmpl_id.image_ids.product_variant_ids",
    )
    def _compute_image_ids(self):
        for product in self:
            images = product.product_tmpl_id.image_ids.filtered(
                lambda x: (
                    not x.product_variant_ids or product.id in x.product_variant_ids.ids  # noqa: B023
                )
            )
            product.image_ids = [(6, 0, images.ids)]
            if product.image_ids:
                product.image_1920 = (
                    product.image_ids[0].with_context(bin_size=False).image_1920
                )

    def _inverse_image_ids(self):
        for product in self:
            # Remember the list of images that were before changes
            previous_images = product.product_tmpl_id.image_ids.filtered(
                lambda x: (
                    not x.product_variant_ids or product.id in x.product_variant_ids.ids  # noqa: B023
                )
            )
            for image in product.image_ids:
                if isinstance(image.id, models.NewId):
                    # Image added
                    image.owner_id = product.product_tmpl_id.id
                    image.owner_model = "product.template"
                    image.product_variant_ids = [(6, 0, product.ids)]
                    image.create(image._convert_to_write(image._cache))
                else:
                    previous_images -= image
                    # Update existing records
                    image.write(image._convert_to_write(image._cache))
            for image in previous_images:
                # Images removed
                if not image.product_variant_ids:
                    variants = product.product_tmpl_id.product_variant_ids
                else:
                    variants = image.product_variant_ids
                variants -= product
                if not variants:
                    # Remove the image, as there's no variant that contains it
                    image.unlink()
                else:
                    # Leave the images for the rest of the variants
                    image.product_variant_ids = [(6, 0, variants.ids)]
            product.image_1920 = (
                False if len(product.image_ids) < 1 else product.image_ids[0].image_1920
            )

    def unlink(self):
        obj = self.with_context(bypass_image_removal=True)
        # Remove images that are linked only to the product variant
        for product in self:
            images2remove = product.image_ids.filtered(
                lambda image: (
                    product in image.product_variant_ids  # noqa: B023
                    and len(image.product_variant_ids) == 1
                )
            )
            images2remove.unlink()
        # We need to pass context to super so this syntax is valid
        return super(ProductProduct, obj).unlink()
