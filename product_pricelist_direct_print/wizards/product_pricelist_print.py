# -*- coding: utf-8 -*-
# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class ProductPricelistPrint(models.TransientModel):
    _name = 'product.pricelist.print'

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )
    categ_ids = fields.Many2many(
        comodel_name='product.category',
        string='Categories',
    )
    show_variants = fields.Boolean()
    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        string='Products',
        help='Keep empty for all products',
    )
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Products',
        help='Keep empty for all products',
    )
    show_standard_price = fields.Boolean(string='Show Cost Price')
    show_sale_price = fields.Boolean(string='Show Sale Price')

    @api.model
    def default_get(self, fields):
        res = super(ProductPricelistPrint, self).default_get(fields)
        if self.env.context.get('active_model') == 'product.template':
            res['product_tmpl_ids'] = [
                (6, 0, self.env.context.get('active_ids', []))]
        elif self.env.context.get('active_model') == 'product.product':
            res['show_variants'] = True
            res['product_ids'] = [
                (6, 0, self.env.context.get('active_ids', []))]
        elif self.env.context.get('active_model') == 'product.pricelist':
            res['pricelist_id'] = self.env.context.get('active_id', False)
        elif self.env.context.get('active_model') == 'res.partner':
            res['partner_id'] = self.env.context.get('active_id', False)
            partner = self.env['res.partner'].browse(
                self.env.context.get('active_id', False))
            res['pricelist_id'] = partner.property_product_pricelist.id
        return res

    @api.multi
    def print_report(self):
        if not(self.pricelist_id or self.show_standard_price or
               self.show_sale_price):
            raise ValidationError(_(
                'You must set price list or any show price option.'))
        return self.env['report'].get_action(
            self, 'product_pricelist_direct_print.report_product_pricelist')
