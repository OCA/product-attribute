# Copyright 2023 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductSupplierinfoFake(models.Model):
    _name = "product.supplierinfo.fake"
    _inherit = ["product.supplierinfo", "attribute.value.dependant.mixin"]
    _description = "Product supplierinfo fake model for tests"
