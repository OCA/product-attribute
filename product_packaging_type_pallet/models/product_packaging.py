# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    is_pallet = fields.Boolean()


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    type_is_pallet = fields.Boolean(related="packaging_type_id.is_pallet")
    layers = fields.Integer()
    packs_per_layer = fields.Integer(help="number of boxes/bags on a layer")
