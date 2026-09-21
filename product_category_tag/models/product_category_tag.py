# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from random import randint

from odoo import fields, models


class ProductCategoryTag(models.Model):
    _name = "product.category.tag"
    _description = "Product Category Tag"

    name = fields.Char(required=True, translate=True)

    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer(default=lambda self: self._get_default_color())

    _sql_constraints = [
        ("category_tag_name_uniq", "unique (name)", "Tag name already exists!"),
    ]
