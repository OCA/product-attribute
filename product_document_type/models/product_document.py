# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductDocument(models.Model):
    _inherit = "product.document"

    document_type_id = fields.Many2one("product.document.type", index=True)
