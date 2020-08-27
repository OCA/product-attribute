# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    has_multiple_variants = fields.Boolean(compute="_compute_has_variants")
    supplierinfo_group_ids = fields.One2many(
        "product.supplierinfo.group", "product_tmpl_id"
    )

    def _compute_has_variants(self):
        for rec in self:
            rec.has_multiple_variants = len(rec.product_variant_ids) > 1
