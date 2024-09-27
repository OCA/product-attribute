#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    extra_price_formula = fields.Text(
        string="Formula for extra price",
        help="The price computed by this formula is added to the 'Extra price'.\n"
        "Formula evaluated when computing "
        "a dynamic extra price "
        "of this product template attribute value.\n"
        "The following variables are available:\n"
        "- product: the product this attribute value is applied to,\n"
        "- ptav: this product template attribute value.\n"
        "The computed price "
        "must be assigned to the `price` variable.",
    )

    @api.constrains(
        "extra_price_formula",
    )
    def _constrain_extra_price_formula(self):
        """Check syntax of added formula for 'exec' evaluation."""
        pav_model = self.env["product.attribute.value"]
        for ptav in self.filtered("extra_price_formula"):
            pav_model._validate_extra_price_formula(ptav.extra_price_formula)

    def _eval_extra_price_formula_variables_dict(self, product, **additional_variables):
        """Variables described in `product.attribute.extra_price_formula`."""
        self.ensure_one()
        return {
            "product": product,
            "ptav": self,
            **additional_variables,
        }

    def _eval_extra_price_formula(self, product, **additional_variables):
        self.ensure_one()
        extra_price_formula = self.extra_price_formula
        if extra_price_formula:
            variables_dict = self._eval_extra_price_formula_variables_dict(
                product,
                **additional_variables,
            )
            safe_eval(
                extra_price_formula,
                globals_dict=variables_dict,
                mode="exec",
                nocopy=True,
            )
            price = variables_dict.get("price", 0)
        else:
            price = 0
        return price

    @api.model_create_multi
    def create(self, vals_list):
        ptavs = super().create(vals_list)
        for ptav in ptavs:
            ptav.extra_price_formula = (
                ptav.product_attribute_value_id.extra_price_formula
            )
        return ptavs
