# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re
from collections import defaultdict

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.constrains("default_code", "active")
    def _check_product_code_regex_validation(self):
        products_by_category = defaultdict(lambda: self.env["product.product"])
        for rec in self:
            if not rec.default_code or not rec.active:
                continue
            products_by_category[rec.categ_id] |= rec
        for product_category, products in products_by_category.items():
            if not product_category.product_code_regex_validation:
                continue
            pattern = re.compile(product_category.product_code_regex_validation)
            for prod in products:
                if not re.fullmatch(pattern, prod.default_code):
                    raise ValidationError(
                        _("Product Code %s does not match the Product Category format.")
                        % prod.default_code
                    )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.constrains("categ_id")
    def _check_product_code_regex_validation(self):
        return self.mapped("product_variant_ids")._check_product_code_regex_validation()
