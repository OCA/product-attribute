# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    tracking = fields.Selection(
        selection=lambda x: x._get_tracking_values_from_product()
    )

    @api.model
    def _get_tracking_values_from_product(self):
        return self.env["product.template"]._fields["tracking"].selection
