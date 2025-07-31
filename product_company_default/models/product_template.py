# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_id = fields.Many2one(default=lambda self: self._default_company_id())

    @api.model
    def _default_company_id(self):
        context = self.env.context
        if tools.config["test_enable"] and not context.get(
            "test_product_company_default"
        ):
            return False
        return self.env.company
