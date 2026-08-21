# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _inverse_product_state_id(self):
        """Keep sale_ok in sync with the state restriction."""
        super()._inverse_product_state_id()
        for template in self:
            if template.product_state_id:
                template.sale_ok = not template.product_state_id.restrict_sale