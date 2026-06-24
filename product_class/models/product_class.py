# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductClass(models.Model):
    _name = "product.class"
    _description = "Product Class"
    _order = "name"

    _name_uniq = models.Constraint(
        "unique(name)",
        "A product class with this name already exists.",
    )

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    attribute_line_ids = fields.One2many(
        comodel_name="product.class.attribute.line",
        inverse_name="class_id",
        string="Attributes",
        help="Allowed attributes for products of this"
        "class and whether they are required.",
    )

    @api.constrains("attribute_line_ids")
    def _check_attribute_ids_used_by_products(self):
        for product_class in self:
            class_attribute_ids = product_class.attribute_line_ids.attribute_id.ids
            invalid_lines = self.env["product.template.attribute.line"].search(
                [
                    ("product_tmpl_id.class_id", "=", product_class.id),
                    ("attribute_id", "not in", class_attribute_ids),
                ]
            )
            if not invalid_lines:
                continue

            invalid_names = ", ".join(
                sorted(set(invalid_lines.mapped("attribute_id.display_name")))
            )
            raise ValidationError(
                self.env._(
                    "Cannot remove attributes used in products assigned to class "
                    "'%(product_class)s': %(attrs)s. Please remove these attributes "
                    "or change the product class.",
                    product_class=product_class.name,
                    attrs=invalid_names,
                )
            )
