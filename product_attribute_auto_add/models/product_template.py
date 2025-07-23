# Copyright Cetmix OU 2025
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    disable_attribute_autoupdate = fields.Boolean(
        help="Exclude this product from automatic addition of new attribute values.",
        default=False,
    )
