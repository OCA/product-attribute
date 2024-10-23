# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    company_id = fields.Many2one(default=lambda self: self._default_company_id())

    @api.model
    def _default_company_id(self):
        # Get the system parameter configuration
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_company_default.default_company_enable")
        )
        if param == "1":
            return self.env.company
        return False
