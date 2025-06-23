# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    can_be_purchased = fields.Boolean(
        compute="_compute_can_be_purchased",
        readonly=False,
        store=True,
        help="If true, the packaging can be used for purchase orders",
    )

    @api.depends("packaging_level_id")
    def _compute_can_be_purchased(self):
        for record in self:
            record.can_be_purchased = record.packaging_level_id.can_be_purchased
