# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductAttributeValueFakeRecord(models.Model):
    """A record of another module pointing to attribute values, such as a lot
    keeping the fishing area of its product."""

    _name = "product.attribute.value.fake.record"
    _description = "Record pointing to attribute values"

    name = fields.Char()
    value_id = fields.Many2one(comodel_name="product.attribute.value")
    company_value_id = fields.Many2one(
        comodel_name="product.attribute.value", company_dependent=True
    )
    product_id = fields.Many2one(comodel_name="product.product", ondelete="restrict")
    value_ids = fields.Many2many(
        string="Values",
        comodel_name="product.attribute.value",
        relation="product_attribute_value_fake_record_rel",
        column1="record_id",
        column2="value_id",
    )
