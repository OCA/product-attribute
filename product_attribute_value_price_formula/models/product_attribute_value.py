#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import test_python_expr


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    extra_price_formula = fields.Text(
        string="Formula for extra price",
        help="The price computed by this formula is added to the 'Extra price'.\n"
        "Formula evaluated when computing "
        "a dynamic extra price "
        "of this attribute value.\n"
        "The following variables are available:\n"
        "- product: the product this attribute value is applied to,\n"
        "- ptav: the template attribute value corresponding to this value.\n"
        "The computed price "
        "must be assigned to the `price` variable.",
    )

    @api.model
    def _validate_extra_price_formula(self, extra_price_formula):
        error_message = test_python_expr(
            expr=extra_price_formula,
            mode="exec",
        )
        if error_message:
            raise ValidationError(error_message)
        return True

    @api.constrains(
        "extra_price_formula",
    )
    def _constrain_extra_price_formula(self):
        """Check syntax of added formula for 'exec' evaluation."""
        pav_model = self.env["product.attribute.value"]
        for attribute in self.filtered("extra_price_formula"):
            pav_model._validate_extra_price_formula(attribute.extra_price_formula)
