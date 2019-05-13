# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring
from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def name_get(self):
        result = []
        for this in self:
            name_result = super(ProductProduct, this).name_get()
            return_val_split = name_result[0][1].split()
            for element in return_val_split:
                if element == "[%s]" % this.default_code:
                    return_val_split.remove(element)
                result.append((this.id, ' '.join(return_val_split)))
        return result
