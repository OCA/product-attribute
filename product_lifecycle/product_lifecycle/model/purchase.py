# coding: utf-8
###############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://www.vauxoo.com>).
#    All Rights Reserved
###############################################################################
#    Credits:
#    Coded by: Katherine Zaoral <kathy@vauxoo.com>
#    Planified by: Nhomar Hernandez <nhomar@vauxoo.com>
#    Audited by: Nhomar Hernandez <nhomar@vauxoo.com>
###############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

from openerp import models, fields, api, exceptions, _


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def write(self, values):
        """
        First check that the purchase order lines have not discontinued
        product.
        """
        order_lines = values.get('order_line', [])
        obsolete = []
        for line in order_lines:
            if isinstance(line[2], dict):
                product_id = line[2].get('product_id', False)
                sequence = line[2].get('sequence', False)
                if product_id:
                    product = self.env['product.product'].browse(product_id)
                    if product.state2 == 'obsolete':
                        obsolete.append((sequence, product))
        if obsolete:
            obsolete.sort()
            obsolete_msg = str()
            for item in obsolete:
                obsolete_msg += ' '.join(['\n', '-', _('Line'), str(item[0]),
                                          _('with product'), item[1].name])
            raise exceptions.Warning('\n'.join([
                _('Purchase order line can not have discontinued products.'),
                _('The next lines cannot be added to the purchase order:'),
                obsolete_msg]))
        return super(PurchaseOrder, self).write(values)


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    discontinued_product_id = fields.Many2one(
        'product.product', string='Discontinued Product',
        domain=[('state2', 'in', ['obsolete'])],
        help='When introduce a discontinued product to the product field in'
             ' the purchase order line then will raise a warning and will auto'
             ' fill this field with the discontiued product and clean the'
             ' product field so you can add the replacement product')

    @api.v7
    def onchange_product_id(
            self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, state='draft',
            context=None):
        """
        Raise a exception is you select discontinued product.
        Auto fill the discontinued_product_id field with the value given in
        product.
        """
        context = context or {}
        product_obj = self.pool.get('product.product')
        res = super(PurchaseOrderLine, self).onchange_product_id(
            cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=date_order,
            fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit, state=state, context=context)
        res.get('domain', dict()).update({'product_id': []})

        if product:
            product_brw = product_obj.browse(cr, uid, product, context=context)
            if product_brw.state2 in ['obsolete']:
                replacements = product_brw.get_good_replacements()
                msg = (product_brw.display_name + " " +
                       _('is a discontinued product.') + '\n')
                if replacements:
                    msg += _('Select one of the replacement products.')
                else:
                    msg += ('\n' * 2 + _(
                        'The are not replacement products defined for the'
                        ' product you selected. Please select another product'
                        ' or define a replacement product in the product form'
                        ' view.'))
                res.update({'warning': {'title': 'Error!', 'message': msg}})
                res.get('value').update({
                    'discontinued_product_id': product})
        return res

    @api.onchange('discontinued_product_id')
    def onchange_discontinued_product_id(self):
        """
        - clean the product_id field.
        - add a domain to the product_id field to show only the replacements
        for the current discontinued product.
        """
        res = {'domain': {'product_id': []}}
        if self.discontinued_product_id:
            self.product_id = False
            replacements = self.discontinued_product_id.get_good_replacements()
            res.get('domain').update({
                'product_id': [('id', 'in', replacements)]})
        return res
