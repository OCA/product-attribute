# -*- coding: utf-8 -*-
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    stock_state_threshold = fields.Float(
        help="Define custom value under wich the stock state of the products"
        " of this category will pass from 'In Stock' to 'In Limited Stock'"
        " State. If not set, Odoo will use the value defined for the company")
