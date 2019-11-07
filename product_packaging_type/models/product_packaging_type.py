# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ProductPackagingType(models.Model):
    _name = "product.packaging.type"
    _description = "Type management for product.packaging"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    # required = fields.Boolean()
    active = fields.Boolean(default=True)


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_type_id = fields.Many2one(
        "product.packaging.type",
        required=True,
        ondelete="restrict"
    )
    type_has_gtin = fields.Boolean(related="packaging_type_id.has_gtin",
                                   readonly=True)
    sequence = fields.Integer(related="packaging_type_id.sequence")
