#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    ptav_formula_extra_price = fields.Float(
        string="Formula Price Extra",
        help="Extra price computed from formula of attribute values.",
        compute="_compute_ptav_formula_extra_price",
        digits="Product Price",
    )

    @api.depends(
        "ptav_formula_extra_price",
    )
    def _compute_ptav_formula_extra_price(self):
        for product in self:
            formula_extra_price = 0
            for ptav in product.product_template_attribute_value_ids:
                formula_extra_price += ptav._eval_extra_price_formula(
                    product=product,
                )
            product.ptav_formula_extra_price = formula_extra_price

    @api.depends(
        "ptav_formula_extra_price",
    )
    def _compute_product_price_extra(self):
        res = super()._compute_product_price_extra()
        for product in self:
            product.price_extra += product.ptav_formula_extra_price
        return res
