# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _create_variant_ids(self):
        """prevent variant creation at product merge process"""
        if self.env.context.get("product_merge"):
            return
        return super()._create_variant_ids()
