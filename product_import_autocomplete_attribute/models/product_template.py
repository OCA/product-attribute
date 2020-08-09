# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def sync_attrs_from_variants(self):
        for rec in self.with_context({"from_sync_attrs_from_variants": True}):
            variant_attr_values = rec.product_variant_ids.mapped(
                "attribute_value_ids"
            )
            variant_attrs = variant_attr_values.mapped("attribute_id")
            for vattr in variant_attrs:
                tmpl_attr_line = rec.attribute_line_ids.filtered(
                    lambda r: r.attribute_id == vattr
                )
                possible_values = variant_attr_values.filtered(
                    lambda r: r.attribute_id == vattr
                )
                if not tmpl_attr_line:
                    self.env["product.template.attribute.line"].create(
                        {
                            "product_tmpl_id": rec.id,
                            "attribute_id": vattr.id,
                            "value_ids": [(6, 0, possible_values.ids)],
                        }
                    )
                else:
                    tmpl_attr_line.value_ids |= possible_values
            # with new attributes, re-check validity of deactivated variants,
            # create deactivated other possible variants
            rec.create_variant_ids()
