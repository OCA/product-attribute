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

        # Collect all attribute_id and product_tmpl_id
        attribute_ids = [attr.id for attr in auto_add_map]
        product_tmpl_ids = []
        for attr in auto_add_map:
            templates = attr.product_tmpl_ids.filtered(
                lambda tmpl: not tmpl.disable_attribute_autoupdate
            )
            product_tmpl_ids.extend(templates.ids)

        # Global search for all needed lines
        lines = attribute_line_obj.search(
            [
                ("attribute_id", "in", attribute_ids),
                ("product_tmpl_id", "in", product_tmpl_ids),
            ]
        )

        # Group lines by attribute_id
        lines_by_attr = defaultdict(attribute_line_obj.browse)
        for line in lines:
            lines_by_attr[line.attribute_id.id] |= line

        # In the loop, filter and update only the needed lines
        for attribute, values in auto_add_map.items():
            attr_lines = lines_by_attr.get(attribute.id)
            if not attr_lines:
                continue
            valid_lines = attr_lines.filtered(
                lambda line_, attr=attribute: line_.product_tmpl_id
                in attr.product_tmpl_ids
            )
            valid_lines.write({"value_ids": [(4, v.id) for v in values]})
        return results
