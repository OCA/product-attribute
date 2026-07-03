# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeTemplate(models.Model):
    _name = "product.attribute.template"
    _description = "Product Attribute Template"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        help="Leave empty to make it available for all companies.",
    )
    line_ids = fields.One2many(
        "product.attribute.template.line",
        "template_id",
        string="Attributes",
        copy=True,
    )

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "A template with the same name already exists for this company.",
        )
    ]


class ProductAttributeTemplateLine(models.Model):
    _name = "product.attribute.template.line"
    _description = "Product Attribute Template Line"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    template_id = fields.Many2one(
        "product.attribute.template",
        required=True,
        ondelete="cascade",
    )
    attribute_id = fields.Many2one(
        "product.attribute",
        string="Attribute",
        required=True,
        help="Attribute to be added to the product when applying this template.",
    )

    _sql_constraints = [
        (
            "template_attribute_uniq",
            "unique(template_id, attribute_id)",
            "This attribute is already included in the template.",
        )
    ]
