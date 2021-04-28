# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    _sql_constraints = [
        (
            "default_code_uniq",
            "unique(default_code)",
            "Internal Reference must be unique across the database!",
        )
    ]

    @api.constrains('default_code', 'active')
    def check_unique_company_and_default_code(self):
        for rec in self:
            if rec.active and rec.default_code:
                filters = [
                    ('default_code', '=', rec.default_code),
                    ('active', '=', True)]
                products = self.search(filters)
                if len(products) > 1:
                    raise ValidationError(_(
                        'There can not be two active products with the same Reference code.'))
