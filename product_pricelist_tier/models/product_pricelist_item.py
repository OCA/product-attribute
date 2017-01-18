# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError


class PricelistItem(models.Model):

    _inherit = 'product.pricelist.item'

    compute_price = fields.Selection(
        selection_add=[
            ('tiered', 'Tiered Price'),
        ],
    )
    tiered_price = fields.Float(
        string='Tiered Price',
        digits=dp.get_precision('Product Price'),
        help='The desired price at minimum quantity you specify. '
        'e.g. You want 10 bowls to cost a total of $20. '
        'Set this field to 20, and set minimum quantity to 10. The '
        'price discount will automatically be calculated for you.',
        store=True,
    )

    @api.onchange('compute_price', 'tiered_price')
    def _onchange_compute_price(self):
        if self.compute_price != 'tiered':
            self.tiered_price = 0.0
        return super(PricelistItem, self)._onchange_compute_price()

    @api.constrains('compute_price', 'min_quantity')
    def _check_min_quantity(self):
        if self.compute_price == 'tiered':
            if not self.min_quantity:
                raise ValidationError(_(
                    'Must include minimum quantity of 1 or '
                    'more if pricing is tiered'
                ))

    @api.constrains('compute_price', 'applied_on')
    def _check_applied_on(self):
        if self.compute_price == 'tiered':
            if self.applied_on != '1_product':
                raise ValidationError(_(
                    'The pricelist item can only be applied on product if '
                    'compute price is tiered. Set `Apply On` to `Product` '
                    'if you want a tiered price.'
                ))

    @api.onchange(
        'tiered_price',
        'min_quantity',
        'compute_price',
        'product_tmpl_id',
        'applied_on')
    def _onchange_price_discount(self):
        if self.compute_price == 'tiered':
            self.base = 'list_price'

            self._check_min_quantity()
            self._check_applied_on()

            normal_unit_price = self.product_tmpl_id.list_price
            discount_unit_price = self.tiered_price / self.min_quantity

            if normal_unit_price:
                self.price_discount = \
                    (1 - (discount_unit_price / normal_unit_price)) * 100
            else:
                self.price_discount = 0.0
