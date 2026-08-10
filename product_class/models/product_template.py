# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    class_id = fields.Many2one(
        comodel_name="product.class",
        string="Product Class",
        help="Product class that constrains which attributes can be used",
    )

    class_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        compute="_compute_class_attribute_ids",
        string="Class Attributes",
        help="Attributes allowed by the selected product class",
    )

    class_required_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        compute="_compute_class_attribute_ids",
        string="Class Required Attributes",
        help="Required attributes for the selected product class.",
    )

    @api.depends(
        "class_id",
        "class_id.attribute_line_ids",
        "class_id.attribute_line_ids.attribute_id",
        "class_id.attribute_line_ids.required",
    )
    def _compute_class_attribute_ids(self):
        for product in self:
            if not product.class_id:
                product.class_attribute_ids = False
                product.class_required_attribute_ids = False
                continue

            class_lines = product.class_id.attribute_line_ids
            product.class_attribute_ids = class_lines.attribute_id
            product.class_required_attribute_ids = class_lines.filtered(
                "required"
            ).attribute_id

    @api.onchange("class_id")
    def _onchange_class_id_prefill_attribute_lines(self):
        """Suggest the class required attributes on the product.

        Values are deliberately left empty: the user must pick them before the
        product can be saved. The suggestions are dropped when the class is
        changed or cleared, as long as the user didn't fill any line in.
        """
        if self.attribute_line_ids.value_ids:
            # The user already started filling lines in, leave their work alone.
            return
        attributes = self.class_required_attribute_ids
        if not (attributes or self.attribute_line_ids):
            return
        self.attribute_line_ids = [
            Command.clear(),
            *(
                Command.create({"attribute_id": attribute.id})
                for attribute in attributes
            ),
        ]

    @api.constrains("class_id", "attribute_line_ids")
    def _check_class_attributes(self):
        """
        Ensure all attribute_line_ids belong to the selected class.
        """
        for product in self:
            if not product.class_id:
                continue

            class_attributes = product.class_attribute_ids
            invalid_attributes = (
                product.attribute_line_ids.attribute_id - class_attributes
            )

            if invalid_attributes:
                invalid_names = ", ".join(invalid_attributes.mapped("display_name"))
                raise ValidationError(
                    self.env._(
                        "Product '%(product)s' has attribute lines that do not belong "
                        "to the selected class '%(product_class)s': %(attrs)s. "
                        "Please remove these attributes or change the product class.",
                        product=product.name,
                        product_class=product.class_id.name,
                        attrs=invalid_names,
                    )
                )

            required_attributes = product.class_required_attribute_ids
            missing_attributes = (
                required_attributes - product.attribute_line_ids.attribute_id
            )

            if missing_attributes:
                missing_names = ", ".join(
                    sorted(missing_attributes.mapped("display_name"))
                )
                raise ValidationError(
                    self.env._(
                        "Product '%(product)s' is missing required attributes "
                        "for the selected class '%(product_class)s': %(attrs)s.",
                        product=product.name,
                        product_class=product.class_id.name,
                        attrs=missing_names,
                    )
                )
