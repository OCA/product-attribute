# Copyright 2025 ForgeFlow (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    uom_id = fields.Many2one(
        "uom.uom",
        "Default Unit of Measure",
        help="Default unit of measure used for products in this category.",
    )

    def update_product_uom(self):
        products = self.env["product.template"].search([("categ_id", "in", self.ids)])
        if not products:
            return True
        return products.set_uom_from_category()
