# Copyright 2025 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    battery_ids = fields.One2many(
        "product.battery",
        "product_tmpl_id",
        string="Battery",
    )
