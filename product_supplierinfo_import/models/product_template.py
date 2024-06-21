# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    created_from_supplierinfo_import = fields.Boolean(
        help="This product was created with the vendor import wizard"
    )
