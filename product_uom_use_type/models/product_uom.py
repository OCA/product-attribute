# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    use_type = fields.Selection(
        [('sale', 'Unit available for sales'),
         ('purchase', 'Unit available for purchases'),
         ('both', 'Unit available for sales and purchases')],
        required=True, default='both')
