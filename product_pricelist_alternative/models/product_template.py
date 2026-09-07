# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_product_price_context(self, combination):
        # OVERRIDE: to keep the selected sale configurator combination in
        # the context so alternative pricelist rules can resolve the variant.
        res = super()._get_product_price_context(combination)
        if combination:
            res["product_pricelist_alternative_combination_ids"] = tuple(
                combination.ids
            )
        return res
