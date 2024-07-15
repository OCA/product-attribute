# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Mathieu Delva <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    weight = fields.Float(default=0)
    product_tmpl_weight = fields.Float(
        compute="_compute_product_tmpl_weight", string="Template Weight"
    )  # afficher que si poid >0 + ajouter label

    def _compute_product_tmpl_weight(self):
        for record in self:
            record.product_tmpl_weight = record.product_tmpl_id.weight
