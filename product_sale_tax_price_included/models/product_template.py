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
        compute='_compute_price_vat_incl_excl', multi='price_vat_incl_excl',
        string='Sale Price Taxes Excluded',
        )
    price_vat_incl = fields.Float(
        compute='_compute_price_vat_incl_excl', multi='price_vat_incl_excl',
        string='Sale Price Taxes Included',
        )

    @api.multi
    @api.depends('list_price', 'taxes_id', 'taxes_id.type', 'taxes_id.amount')
    def _compute_price_vat_incl_excl(self):
        for template in self:
            info = template.taxes_id.compute_all(template.list_price, 1)
            template.price_vat_incl = info['total_included']
            template.price_vat_excl = info['total']

    @api.multi
    @api.depends('taxes_id')
    def _compute_sale_tax_price_include(self):
        for template in self:
            sale_tax_price_include = ''

            if not template.taxes_id:
                template.sale_tax_price_include = 'no_tax'
            else:
                for taxes in template.taxes_id:
                    if sale_tax_price_include == '':
                        if taxes.price_include:
                            sale_tax_price_include = 'all_tax_incl'
                        else:
                            sale_tax_price_include = 'all_tax_excl'
                    elif taxes.price_include:
                        if sale_tax_price_include == 'all_tax_incl':
                            sale_tax_price_include = 'all_tax_incl'
                        else:
                            sale_tax_price_include = 'various_taxes'
                    else:
                        if sale_tax_price_include == 'all_tax_excl':
                            sale_tax_price_include = 'all_tax_excl'
                        else:
                            sale_tax_price_include = 'various_taxes'
                    template.sale_tax_price_include = sale_tax_price_include
