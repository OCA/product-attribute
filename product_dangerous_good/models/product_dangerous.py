# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models, fields


class ProductDangerousClass(models.Model):
    _name = "product.dangerous.class"
    _description = "Product Dangerous Class"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    image = fields.Binary(string="Icon", required=True)
    class_type = fields.Many2one(
        comodel_name="product.dangerous.class.type",
        ondelete="restrict",
        string="Dangerous Type",
    )

    _sql_constraints = [
        ("code_unique", "unique(code)", "This code already exist")
    ]


class ProductDangerousClassType(models.Model):
    _name = "product.dangerous.class.type"
    _description = "Product Dangerous Type"

    name = fields.Char(required=True)
    division = fields.Char()
