# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    required = fields.Boolean()

    @api.model
    def cron_check_create_required_packaging(self):
        """Create required packaging for each consumable product if missing."""
        existing_products = self.env["product.product"].search(
            [("type", "in", ("product", "consu"))]
        )
        required_packaging_types = self.search([("required", "=", True)])
        packaging_model = self.env["product.packaging"]
        create_values = []
        for product in existing_products:
            packagings = product.packaging_ids
            existing_packaging_types = packagings.mapped("packaging_type_id")
            missing_packaging_types = (
                required_packaging_types - existing_packaging_types
            )
            if not missing_packaging_types:
                continue
            create_values.extend(
                [
                    ptype._prepare_required_packaging_vals(product)
                    for ptype in missing_packaging_types
                ]
            )
        if create_values:
            # TODO: consider using queue.job to split this in smaller chunks
            # and have less impact on perf.
            packaging_model.create(create_values)
            msg = f"CREATED {len(create_values)} required packaging"
            _logger.info(msg)
            return msg
        return True

    def _prepare_required_packaging_vals(self, product):
        res = {
            "packaging_type_id": self.id,
            "name": self.name,
            "product_id": product.id,
        }
        return res
