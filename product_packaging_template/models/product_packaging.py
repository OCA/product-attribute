# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    packaging_tmpl_id = fields.Many2one("product.packaging.template", readonly=True)
