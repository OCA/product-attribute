# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    product_brand_ids = fields.One2many(
        comodel_name="product.brand",
        inverse_name="company_id",
        string="Brands",
    )
