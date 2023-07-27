# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    active = fields.Boolean(default=True)
