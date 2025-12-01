# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    active = fields.Boolean(default=True)
