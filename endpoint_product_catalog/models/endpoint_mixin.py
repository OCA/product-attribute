# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class EndpointMixin(models.AbstractModel):
    _inherit = "endpoint.mixin"

    product_assortment_id = fields.Many2one(
        "ir.filters",
        domain=[("is_assortment", "=", True)],
    )
    include_prices = fields.Boolean()
