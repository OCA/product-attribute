# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def _inverse_product_state_id(self):
        for product in self:
            if product.active and product.product_state_id.deactivate_product:
                product.active = False
            if not product.active and product.product_state_id.activate_product:
                product.active = True
