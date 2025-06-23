# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.fields import first


class ProductTemplate(models.Model):
    _inherit = "product.template"

    created_from_supplierinfo_import = fields.Boolean(
        help="This product was created with the vendor import wizard"
    )

    product_code = fields.Char(
        compute="_compute_product_code",
        help="This is the supplier product code from Main Supplier.",
        compute_sudo=False,
        search="_search_product_code",
        readonly=True,
    )

    def _compute_product_code(self):
        for prod in self:
            seller = first(prod.seller_ids)
            prod.product_code = seller.product_code

    @api.model
    def _search_product_code(self, operator, value):
        return [("seller_ids.product_code", operator, value)]
