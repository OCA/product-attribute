# Copyright Cetmix OU 2025
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from collections import defaultdict

from odoo import api, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create new attribute values and automatically add them to product templates.

        This method extends the standard create method to automatically add new
        attribute values to all product templates that use the corresponding attribute,
        if the attribute has attribute_line_auto_add flag set to True.

        Args:
            vals_list (list): List of dictionaries containing the values to create.

        Returns:
            recordset: The newly created attribute values.
        """
        results = super().create(vals_list)
        attribute_line_obj = self.env["product.template.attribute.line"]
        auto_add_map = defaultdict(results.browse)
        for record in results.filtered("attribute_id.attribute_line_auto_add"):
            auto_add_map[record.attribute_id] |= record

        for attribute, values in auto_add_map.items():
            lines = attribute_line_obj.search(
                [
                    ("product_tmpl_id", "in", attribute.product_tmpl_ids.ids),
                    ("attribute_id", "=", attribute.id),
                ]
            )
            lines.write({"value_ids": [(4, v.id) for v in values]})
        return results
