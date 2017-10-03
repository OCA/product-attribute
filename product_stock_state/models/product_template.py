# -*- coding: utf-8 -*-
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_state_threshold = fields.Float(
        help="Define custom value under wich the stock state will pass from"
        " 'In Stock' to 'In Limited Stock' State. If not set, Odoo will"
        " use the value defined in the product category. If"
        " no value is defined in product category, it will use the value"
        " defined for the company")
