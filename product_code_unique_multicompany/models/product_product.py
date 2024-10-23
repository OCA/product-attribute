# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):

    _inherit = "product.product"

    _sql_constraints = [
        (
            "default_code_uniq_multicompany",
            "unique(default_code, company_id)",
            "Internal Reference must be unique per company!",
        )
    ]
