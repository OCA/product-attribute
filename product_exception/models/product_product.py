# Copyright 2021 ForgeFlow (http://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = ["product.product", "base.exception"]
    _name = "product.product"

    exception_ids = fields.Many2many(related="product_tmpl_id.exception_ids")

    def _get_main_records(self):
        return self.mapped("product_tmpl_id")

    @api.model
    def _reverse_field(self):
        return "product_tmpl_ids"

    def _detect_exceptions(self, rule):
        records = super()._detect_exceptions(rule)
        return records.mapped("product_tmpl_id")
