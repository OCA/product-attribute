# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPackagingLevel(models.Model):
    _inherit = "product.packaging.level"

    can_be_purchased = fields.Boolean(string="Can be purchased", default=True)
    packaging_ids = fields.One2many(
        comodel_name="product.packaging", inverse_name="packaging_level_id"
    )
