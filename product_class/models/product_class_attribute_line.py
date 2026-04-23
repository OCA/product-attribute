# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductClassAttributeLine(models.Model):
    _name = "product.class.attribute.line"
    _description = "Product Class Attribute Line"
    _order = "class_id, id"

    _class_attribute_uniq = models.Constraint(
        "unique(class_id, attribute_id)",
        "Each attribute can be configured only once per product class.",
    )

    class_id = fields.Many2one(
        comodel_name="product.class",
        required=True,
        ondelete="cascade",
        index=True,
        string="Product Class",
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute",
        required=True,
        ondelete="restrict",
        index=True,
        string="Attribute",
    )
    required = fields.Boolean(
        default=False,
        help="If enabled, products of this class must define this attribute.",
    )
