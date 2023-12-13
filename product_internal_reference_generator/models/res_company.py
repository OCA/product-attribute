# Copyright 2023 Ooops - Ilyas
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    default_int_ref_template_id = fields.Many2one(
        "product.code.sequence",
        default_model="product.template",
        string="Default Internal Reference Template",
    )
