# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools import safe_eval


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    filter_domain = fields.Char(
        string="Filter",
        default="[]",
        compute="_compute_filter_domain",
        readonly=False,
        store=True
    )

    def _is_applicable_for(self, product, qty_in_product_uom):
        if self.filter_domain != "[]":
            domain = safe_eval.safe_eval(self.filter_domain)
            if not product.filtered_domain(domain):
                return False
        return super()._is_applicable_for(product, qty_in_product_uom)

    @api.depends("applied_on")
    def _compute_filter_domain(self):
        for record in self:
            if record.applied_on != "3_global":
                record.filter_domain = "[]"
