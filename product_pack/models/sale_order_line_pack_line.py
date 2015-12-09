# -*- coding: utf-8 -*-
# Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#                     All Rights Reserved.
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class SaleOrderLinePackLine(models.Model):
    _name = 'sale.order.line.pack.line'
    _description = 'Sale Order Not Detailed Pack Lines'

    order_line_id = fields.Many2one(
        'sale.order.line',
        'Order Line',
        ondelete='cascade',
        required=True)
    product_id = fields.Many2one(
        'product.product',
        'Product',
        required=True)
    price_unit = fields.Float(
        'Unit Price',
        required=True,
        digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float(
        compute="_amount_line",
        string='Subtotal',
        digits=dp.get_precision('Account'))
    product_uom_qty = fields.Float(
        'Quantity',
        digits=dp.get_precision('Product UoS'),
        required=True)

    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        """Recalculate unit price when changing the product."""
        for s in self:
            s.price_unit = s.product_id.lst_price

    @api.multi
    @api.depends('price_unit', 'product_uom_qty')
    def _amount_line(self):
        """Recalculate subtotal price when changing unit price."""
        for s in self:
            s.price_subtotal = s.product_uom_qty * s.price_unit
