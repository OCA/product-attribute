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

    @api.multi
    @api.constrains(
        'compute_price',
        'min_quantity',
        'applied_on',
        'base')
    def _check_fields(self):
        for record in self:
            errors = record._check_tier_validations()
            if errors:
                raise ValidationError(_(errors))

    def _check_tier_validations(self):
        """ Validates conditions for constrains and onchange methods """
        self.ensure_one()
        messages = ''
        onchange_new_vals = {}

        if self.compute_price == 'tiered':
            if self.base != 'list_price':
                messages += (
                    'The pricelist item must be based '
                    'on the product list_price when using '
                    'tiered pricing.\n\n'
                )
                onchange_new_vals['base'] = 'list_price'

            if self.applied_on != '1_product':
                messages += (
                    'The pricelist item can only be applied on product if '
                    'compute price is tiered. Set `Apply On` to `Product` '
                    'if you want a tiered price.\n\n'
                )
                onchange_new_vals['applied_on'] = '1_product'

            if self.min_quantity < 1:
                messages += (
                    'Must include minimum quantity of 1 or '
                    'more if pricing is tiered.\n\n'
                )
                onchange_new_vals['min_quantity'] = 1

        if messages:
            return {
                'warning': {
                    'title': 'Error',
                    'message': messages,
                },
                'value': onchange_new_vals,
            }

    @api.onchange(
        'tiered_price',
        'min_quantity',
        'compute_price',
        'product_tmpl_id',
        'applied_on',
        'base')
    def _onchange_price_discount(self):
        if self.compute_price == 'tiered':
            errors = self._check_tier_validations()
            if errors:
                return errors
            else:
                normal_unit_price = self.product_tmpl_id.list_price
                discount_unit_price = self.tiered_price / self.min_quantity

                if normal_unit_price:
                    self.price_discount = \
                        (1 - (discount_unit_price / normal_unit_price)) * 100
                else:
                    self.price_discount = 0.0
