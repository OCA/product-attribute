# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductRelatedFilterMixin(models.AbstractModel):
    _inherit = "product.related.filter.mixin"
    seller_id = fields.Many2one(
        related='product_id.seller_ids.name',
        string='Product Vendor',
        domain=[('supplier', '=', True)],
    )
