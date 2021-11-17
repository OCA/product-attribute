# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.fields import first


class ProductTemplate(models.Model):

    _inherit = "product.template"

    supplier_product_code = fields.Char(
        compute="_compute_supplier_product_code",
        help="This is the supplier product code from Main Supplier.",
        compute_sudo=False,
        search="_search_supplier_product_code",
        readonly=True,
    )

    def _compute_supplier_product_code(self):
        for prod in self:
            seller = first(prod.seller_ids)
            prod.supplier_product_code = seller.product_code

    @api.model
    def _search_supplier_product_code(self, operator, value):
        return [("seller_ids.product_code", operator, value)]
