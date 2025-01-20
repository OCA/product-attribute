# Copyright 2023 Ooops - Ilyas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("product_tmpl_id"):
                pt = self.env["product.template"].browse(vals["product_tmpl_id"])
                if pt.variants_sequence_id:
                    vals["default_code"] = pt.get_variant_next_default_code()
        return super().create(vals_list)
