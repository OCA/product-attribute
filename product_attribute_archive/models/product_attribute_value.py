# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    active = fields.Boolean(default=True)
