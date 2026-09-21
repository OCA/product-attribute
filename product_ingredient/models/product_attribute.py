# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.tools import ormcache


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.model
    @ormcache()
    def get_allergen_id(self):
        """Helper to get allergen attribute id"""
        return self.env.ref("product_ingredient.product_allergen_attribute").id
