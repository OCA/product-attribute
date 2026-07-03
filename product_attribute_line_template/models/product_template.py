# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_template_id = fields.Many2one(
        "product.attribute.template",
        string="Apply attribute template",
        help=(
            "Select a template to add its attributes to the product. "
            "The selection is cleared after applying."
        ),
    )

    @api.onchange("attribute_template_id")
    def _onchange_attribute_template_id(self):
        for product in self:
            template = product.attribute_template_id
            if not template:
                continue
            # Keep only persisted attribute lines.
            # Any non-saved lines previously added in the form are discarded,
            # so changing the template before saving replaces pending changes.
            persisted_lines = product.attribute_line_ids.filtered(
                lambda line: line._origin.id
            )
            product.attribute_line_ids = persisted_lines
            existing_attr_ids = set(
                product.attribute_line_ids.mapped("attribute_id").ids
            )
            for line in template.line_ids.sorted("sequence"):
                attr_id = line.attribute_id.id
                if attr_id not in existing_attr_ids:
                    product.attribute_line_ids += self.env[
                        "product.template.attribute.line"
                    ].new({"attribute_id": attr_id})
                    existing_attr_ids.add(attr_id)
