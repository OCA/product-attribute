# -*- coding: utf-8 -*-
# Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#                     All Rights Reserved.
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductPackLine(models.Model):
    _name = 'product.pack.line'
    _rec_name = 'product_id'

    parent_product_id = fields.Many2one(
        'product.product',
        'Parent Product',
        ondelete='cascade',
        required=True)
    quantity = fields.Float(
        'Quantity',
        required=True,
        default=1.0)
    product_id = fields.Many2one(
        'product.product',
        'Product',
        ondelete='cascade',
        required=True)

    @api.multi
    def get_sale_order_line_vals(self, line, order):
        self.ensure_one()
        subproduct = self.product_id
        quantity = self.quantity * line.product_uom_qty

        taxes = order.fiscal_position.map_tax(
            subproduct.taxes_id)
        tax_id = [(6, 0, taxes.ids)]

        if subproduct.uos_id:
            uos_id = subproduct.uos_id.id
            uos_qty = quantity * subproduct.uos_coeff
        else:
            uos_id = False
            uos_qty = quantity

        # If pack's price is fixed or totalized, we don't want amount on lines
        if line.product_id.pack_type in [
                'fixed_price', 'totalize_price']:
            price = 0.0
            discount = 0.0
        else:
            price = self.env['product.pricelist'].price_get(
                subproduct.id, quantity,
                order.partner_id.id, context={
                    'uom': subproduct.uom_id.id,
                    'date': order.date_order})[order.pricelist_id.id]
            discount = line.discount

        # Obtain product name in partner's language
        if order.partner_id.lang:
            subproduct = subproduct.with_context(
                lang=order.partner_id.lang)

        return {
            'order_id': order.id,
            'name': '%s%s' % (
                '> ' * (line.pack_depth + 1), subproduct.name
            ),
            'product_id': subproduct.id,
            'price_unit': price,
            'tax_id': tax_id,
            'address_allotment_id': False,
            'product_uom_qty': quantity,
            'product_uom': subproduct.uom_id.id,
            'product_uos_qty': uos_qty,
            'product_uos': uos_id,
            'product_packaging': False,
            'discount': discount,
            'number_packages': False,
            'th_weight': False,
            'state': 'draft',
            'pack_parent_line_id': line.id,
            'pack_depth': line.pack_depth + 1,
        }
