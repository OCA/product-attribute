# Copyright 2020 Versada UAB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategoryAttributeLine(models.Model):
    _name = "product.category.attribute.line"
    _description = "Product Category Attribute Line"
    _sql_constraints = [
        (
            "unique_categ_attr",
            "UNIQUE (category_id, attribute_id)",
            "The category/attribute pairs must be unique!",
        ),
    ]

    category_id = fields.Many2one(
        comodel_name="product.category",
        ondelete="cascade",
        required=True,
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute",
        ondelete="cascade",
        required=True,
    )
    value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Values",
        domain="""[
            ("attribute_id", "=", attribute_id),
        ]""",
    )

    @api.onchange("attribute_id")
    def _onchange_attribute_id(self):
        self.value_ids = self.value_ids.filtered(
            lambda v: v.attribute_id == self.attribute_id
        )
