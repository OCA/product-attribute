# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_tax_price_include = fields.Selection(
        [('no_tax', 'No sale tax'),
         ('all_tax_excl', 'Taxes are not included in sale price'),
         ('all_tax_incl', 'All taxes are included in sale price'),
         ('various_taxes', 'Sale price may include taxes')],
        compute='_compute_sale_tax_price_include',
        string='Taxes in Sale Price',
        help='Indicate if the Sale Price include Taxes or not',
        )

    price_vat_excl = fields.Float(
        compute='_compute_price_vat_excl',
        string='Sale Price Taxes Excluded',
        )
    price_vat_incl = fields.Float(
        compute='_compute_price_vat_incl',
        string='Sale Price Taxes Included',
        )

    @api.depends('list_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_price_vat_excl(self):
        taxes = self.env['account.tax'].browse(self.taxes_id.ids)
        info = taxes.compute_all(self.list_price, 1)
        self.price_vat_excl = info['total']

    @api.depends('list_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_price_vat_incl(self):
        taxes = self.env['account.tax'].browse(self.taxes_id.ids)
        info = taxes.compute_all(self.list_price, 1)
        self.price_vat_incl = info['total_included']

    @api.depends('list_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_price_various_taxes(self):
        taxes = self.env['account.tax'].browse(self.taxes_id.ids)
        info = taxes.compute_all(self.list_price, 1)
        self.price_vat_incl = info['total_included']
        self.price_vat_excl = info['total']

    @api.depends('taxes_id')
    def _compute_sale_tax_price_include(self):
        tmp_sale_tax_price_include = ''

        if not self.taxes_id:
            self.sale_tax_price_include = 'no_tax'
        else:
            for taxes in self.taxes_id:
                if tmp_sale_tax_price_include == '':
                    if taxes.price_include:
                        tmp_sale_tax_price_include = 'all_tax_incl'
                    else:
                        tmp_sale_tax_price_include = 'all_tax_excl'
                elif taxes.price_include:
                    if tmp_sale_tax_price_include == 'all_tax_incl':
                        tmp_sale_tax_price_include = 'all_tax_incl'
                    else:
                        tmp_sale_tax_price_include = 'various_taxes'
                else:
                    if tmp_sale_tax_price_include == 'all_tax_excl':
                        tmp_sale_tax_price_include = 'all_tax_excl'
                    else:
                        tmp_sale_tax_price_include = 'various_taxes'
                self.sale_tax_price_include = tmp_sale_tax_price_include
