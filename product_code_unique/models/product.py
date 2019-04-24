# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)',
         'Internal Reference must be unique across the database!'), ]

    def _check_unique_default_code_insesitive(self):
        for product in self:
            if product.default_code and \
                    self.search_count(
                        [
                            ('default_code', '=ilike',
                             product.default_code),
                            ('id', '!=', product.id)
                        ]) != 0:
                return False
        return True

    _constraints = [
        (_check_unique_default_code_insesitive,
         'Internal Reference must be unique across the database!',
         []),
    ]
