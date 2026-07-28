# Copyright 2023 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSupplierinfoFake(models.Model):
    _name = "product.supplierinfo.fake"
    _inherit = ["product.supplierinfo", "attribute.value.dependent.mixin"]
    _description = "Product supplierinfo fake model for tests"

    name = fields.Char()
