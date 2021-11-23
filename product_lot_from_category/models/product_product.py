# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.onchange("categ_id")
    def _onchange_product_lot_from_category_categ_id(self):
        for product in self.filtered("categ_id.tracking"):
            product.tracking = product.categ_id.tracking
