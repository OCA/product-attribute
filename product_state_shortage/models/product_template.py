# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    def _reset_default_state(self):
        if default_state := self._get_default_product_state():
            self.write({"product_state_id": default_state.id})
