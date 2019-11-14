# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductPackagingType(models.Model):
    _name = "product.packaging.type"
    _description = "Type management for product.packaging"
    _order = 'sequence, code'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    # required = fields.Boolean()
    active = fields.Boolean(default=True)
    is_default = fields.Boolean()


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    @api.model
    def default_packaging_type(self):
        PackType = self.env['product.packaging.type']
        types = PackType.search([('is_default', '=', True)], limit=1)
        if types:
            return types
        types = PackType.search([], limit=1)
        if types:
            return types
        type = PackType.create(
            {
                "name": "Default Type",
                "code": "DEFAULT",
                "sequence": 1,
                "is_default": True,
            }
        )
        return type

    packaging_type_id = fields.Many2one(
        "product.packaging.type",
        required=True,
        ondelete="restrict",
        default=default_packaging_type,
    )
    type_has_gtin = fields.Boolean(related="packaging_type_id.has_gtin",
                                   readonly=True)
    sequence = fields.Integer(related="packaging_type_id.sequence")
