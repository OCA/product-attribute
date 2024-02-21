# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        """Update variant tag_ids after modification in tag_ids"""
        if "tag_ids" in vals:
            old_tag_ids = {
                product_tmpl.id: product_tmpl.tag_ids.ids for product_tmpl in self
            }
        res = super().write(vals)

        if "tag_ids" in vals:
            for product_tmpl in self:
                new_tag_ids = set(product_tmpl.tag_ids.ids)
                previous_tag_ids = set(old_tag_ids[product_tmpl.id])
                tags_to_add = list(new_tag_ids - previous_tag_ids)
                tags_to_remove = list(previous_tag_ids - new_tag_ids)

                for variant in product_tmpl.product_variant_ids:
                    if tags_to_add:
                        variant.tag_ids = [(4, tag_id) for tag_id in tags_to_add]

                    if tags_to_remove:
                        tags_to_remove_variant = (
                            tag_id
                            for tag_id in tags_to_remove
                            if tag_id in variant.tag_ids.ids
                        )
                        variant.tag_ids = [
                            (3, tag_id) for tag_id in tags_to_remove_variant
                        ]
        return res
