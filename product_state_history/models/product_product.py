# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_change_product_state(self):
        self.ensure_one()
        return self.product_tmpl_id.action_change_product_state()
