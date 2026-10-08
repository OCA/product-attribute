# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.translate import html_translate


class ProductProduct(models.Model):
    _inherit = "product.product"

    medical_usage = fields.Html(translate=html_translate)
    medical_contra_indication = fields.Html(translate=html_translate)
    medical_properties = fields.Html(translate=html_translate)
    mecical_composition = fields.Html(translate=html_translate)
    medical_full_description = fields.Html(translate=html_translate)
    medical_indication = fields.Html(translate=html_translate)
    medical_nutritional_value = fields.Html(translate=html_translate)
    medical_legal_text = fields.Html(translate=html_translate)
