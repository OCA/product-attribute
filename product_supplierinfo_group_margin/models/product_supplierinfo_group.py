# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSupplierinfoGroup(models.Model):
    _inherit = "product.supplierinfo.group"

    unit_price_note = fields.Html(string="Unit Prices (Min. Qty / Price / Margin)")
