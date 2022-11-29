# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductPackagingLevel(models.Model):
    _inherit = "product.packaging.level"

    is_pallet = fields.Boolean()
