# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import config


class ProductProduct(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        (
            "default_code_uniq",
            "unique(default_code)",
            "Internal Reference must be unique across the database!",
        )
    ]

    @api.model
    def create(self, vals):
        """
        Avoid create products with the same default code for testing other modules.
        In this common test setup:
        https://github.com/odoo/odoo/blob/15.0/addons/sale/tests/common.py#L99
        Odoo creates three products with the same default_code (FURN_9999) and others.
        If you have installed this module which adds a sql_constraint and use this in
        common setup for testing in your CI will fail.
        """
        if (
            config["test_enable"]
            and "default_code" in vals
            and not self.env.context.get("check_default_code_unique")
        ):
            products = (
                self.env["product.product"]
                .with_context(active_test=False)
                .search([("default_code", "ilike", vals["default_code"])])
            )
            if products:
                vals["default_code"] = vals["default_code"] + "/{}".format(
                    len(products)
                )
        return super().create(vals)
