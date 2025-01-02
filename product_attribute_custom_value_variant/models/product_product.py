# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _unlink_or_archive(self, check_access=True):
        custom_variants_to_keep_ids = self.env.context.get("no_remove_custom_variants")
        return super(
            ProductProduct, self - self.browse(custom_variants_to_keep_ids)
        )._unlink_or_archive(check_access=check_access)
