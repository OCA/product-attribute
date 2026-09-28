# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _create_packaging_from_template(self, template):
        base_values = template._prepare_create_values_for_packaging()
        create_values = []
        for product in self:
            product_values = base_values.copy()
            product_values.update({"product_id": product.id})
            create_values.append(product_values)
        self.env["product.packaging"].create(create_values)

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create all packaging from templates when creating a new variant
        """
        res = super().create(vals_list)
        for variant in res:
            for pt in variant.product_tmpl_id.packaging_tmpl_ids:
                variant._create_packaging_from_template(template=pt)
        return res
