# Copyright 2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import api, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.barcode.required.mixin"]

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        # Try to limit exceptions if we can compute the barcode
        # when products are created via code.
        recs._onchange_code()
        # When automatically created from a template
        # the barcode is not propagated from the template to the variants,
        # thus is pointless to check because it will always fail.
        recs._check_barcode_required()
        return recs

    def write(self, vals):
        res = super().write(vals)
        self._onchange_code()
        self._check_barcode_required()
        return res
