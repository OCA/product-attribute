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

from openerp import models, fields, api, _


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    obsolete = fields.Boolean(
        compute='_check_product_line',
        help='Boolean indicate if the purchase line has a obsolete product')

    @api.depends('product_id')
    def _check_product_line(self):
        """ If product in line is a obsolete product then set the line as
        obsolete True, in other case set to False.
        """
        for line in self:
            line.obsolete = \
                True if line.product_id.state2 == 'obsolete' else False

    @api.v7
    def onchange_product_id(
            self, cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, state='draft',
            context=None):
        """Raise a warning message when the selected product is a obsolete
        product.
        """
        context = context or {}
        product_obj = self.pool.get('product.product')
        res = super(PurchaseOrderLine, self).onchange_product_id(
            cr, uid, ids, pricelist, product, qty, uom,
            partner_id, date_order=date_order,
            fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit, state=state, context=context)
        if product:
            product_brw = product_obj.browse(cr, uid, product, context=context)
            if product_brw.state2 in ['obsolete']:
                replacements = product_brw.get_good_replacements()
                msg = ' '.join([
                    product_brw.display_name, _('is an obsolete product.'),
                    '\n',
                    _('You can force to purchase this item or you can'
                      ' purchase the replacement product')])
                if replacements:
                    msg += '\n' + replacements.display_name
                else:
                    msg += ('\n' * 2 + _(
                        'The are not replacement products defined for the'
                        ' product you selected. You can configure'
                        ' the replacement product in the product form view.'))
                res.update({'warning': {'title': 'Error!', 'message': msg}})
        return res


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    lines_count = fields.Integer(
        compute='_count_pol', string='Purchase Lines Count')

    @api.depends()
    def _count_pol(self):
        """return the quantity of purchase order lines in the purchase order.
        """
        for purchase in self:
            purchase.lines_count = len(purchase.order_line)

    @api.multi
    def lines_open(self):
        """return the view of the purchase order lines.
        """
        return {
            'type': 'ir.actions.act_window',
            'src_model': 'purchase.order',
            'res_model': 'purchase.order.line',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('id', 'in', self.order_line.mapped('id'))],
            'context': {'search_default_order_id': self.id}
        }
