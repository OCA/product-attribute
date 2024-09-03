# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = "product.category"

    product_code_regex_validation = fields.Char(string="Product Code RegEx Validation")

    @api.constrains("product_code_regex_validation")
    def _check_product_code_regex_validation(self):
        for rec in self:
            if not rec.product_code_regex_validation:
                continue
            try:
                pattern = re.compile(rec.product_code_regex_validation)
            except re.error as err:
                raise ValidationError(
                    _("The following regular expression is not valid: %s") % pattern
                ) from err
            products = self.env["product.product"].search([("categ_id", "=", rec.id)])
            for prod in products:
                if not prod.default_code:
                    continue
                if not re.fullmatch(pattern, prod.default_code):
                    raise ValidationError(
                        _("Product Code %s does not match the Product Category format.")
                        % prod.default_code
                    )
