# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def open_packaging_price(self):
        self.ensure_one()
        action = self.env.ref(
            "product_packaging_unit_price_calculator.action_unit_price_wizard"
        ).read()[0]
        action["context"] = {"product_tmpl_id": self.id}
        return action
