# Copyright 2023 Ooops - Ilyas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductCodeSequence(models.Model):
    _name = "product.code.sequence"
    _description = "Internal Reference Template"

    name = fields.Char(required=True)
    sequence_id = fields.Many2one("ir.sequence", required=True)
    variant_reference_numbers = fields.Integer("Digits", default=3, required=True)
