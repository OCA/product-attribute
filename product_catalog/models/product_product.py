# Copyright 2023 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy<raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_catalog_ids = fields.Many2many(
        "product.catalog",
        relation="pp_product_catalog_rel",
        column1="catalog_id",
        column2="product_id",
    )
