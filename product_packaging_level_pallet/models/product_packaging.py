# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    level_is_pallet = fields.Boolean(related="packaging_level_id.is_pallet")
    layers = fields.Integer()
    packs_per_layer = fields.Integer(help="number of boxes/bags on a layer")
