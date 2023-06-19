# Copyright 2019 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = ["product.template", "base.exception"]
    _name = "product.template"

    def check_product_template_cron(self):
        products = self.env["product.template"].search([])
        for product in products:
            product.detect_exceptions()

    def test_button(self):
        products = self.env["product.template"].search([])
        for product in products:
            product.detect_exceptions()

    @api.model
    def _reverse_field(self):
        return "product_tmpl_ids"

    @api.depends("name")
    def detect_exceptions(self):
        all_exceptions = super(ProductTemplate, self).detect_exceptions()
        products = self.mapped("product_variant_ids")
        all_exceptions += products.detect_exceptions()
        return all_exceptions
