# Copyright Cetmix OU 2025
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attribute_line_auto_add = fields.Boolean(
        string="Auto-Add Value to Product Templates",
        help="When enabled new attribute values "
        "will be automatically added to "
        "attribute line in all products templates "
        "that have this attribute.",
    )
