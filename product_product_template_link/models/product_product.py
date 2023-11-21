# Copyright 2019 Alexandre Díaz - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_open_product_template(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": self.product_tmpl_id.id,
            "views": [[False, "form"]],
        }
