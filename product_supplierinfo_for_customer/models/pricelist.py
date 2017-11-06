# -*- coding: utf-8 -*-
# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection([
        ('list_price', 'Public Price'),
        ('standard_price', 'Cost'),
        ('pricelist', 'Other Pricelist'),
        ('partner', 'Partner Prices on the product form')],
        default='list_price', required=True,
        help='Base price for computation.\n'
             'Public Price: The base price will be the Sale/public Price.\n'
             'Cost Price : The base price will be the cost price.\n'
             'Other Pricelist : Computation of the base price based on another'
             ' Pricelist.'
             'Partner Prices: Take the price from the customer info on the'
             ' product form')
