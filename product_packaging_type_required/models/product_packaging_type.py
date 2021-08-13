# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    required = fields.Boolean()

    @api.model
    def cron_check_create_required_packaging(self, limit=0):
        """if limit=0, the method will not apply a limit to process missing
        packages.
        """
        existing_products = self.env["product.product"].search(
            [("type", "in", ("product", "consu"))]
        )
        i = 0
        required_packaging_types = self.search([("required", "=", True)])
        # FIXME: limit is never used and the whole method should be refactored
        for product in existing_products:
            if limit and i == limit:
                break
            packagings = product.packaging_ids
            existing_packaging_types = packagings.mapped("packaging_type_id")
            missing_packaging_types = (
                required_packaging_types - existing_packaging_types
            )
            if not missing_packaging_types:
                continue
            values = [
                ptype.prepare_packaging_vals(product)
                for ptype in missing_packaging_types
            ]
            self.env["product.packaging"].create(values)
        return True

    def prepare_packaging_vals(self, product):
        res = {
            "packaging_type_id": self.id,
            "name": self.name,
            "product_id": product.id,
        }
        return res
