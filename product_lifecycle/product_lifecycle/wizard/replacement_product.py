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
from openerp.exceptions import Warning as UserError, ValidationError


class ReplacementProduct(models.TransientModel):

    """
    Wizard that let to select one of the replacement product of a obsolete
    product.
    """

    _name = 'replacement.product'
    _description = ('Replacement of obsolete products'
                    ' for purchase operations')

    @api.multi
    def _get_lines(self):
        """
        Get the lines with obsolete products

        @return a list of dictionaries to create the new wizard lines.
        """
        res = []

        self.check_active_model()
        order = self._context.get('active_id', False)
        if not order:
            return res
        order = self.env['purchase.order'].browse(order)
        res = [
            (0, 0, {
                'line_id': line.id,
                'number': line.sequence,
                'obsolete_product_id': line.product_id.id,
                'replace_product_id':
                    line.product_id.replaced_by_product_id.id,
            })
            for line in order.order_line
            if line.product_id.state2 in ['obsolete']]
        if not res:
            raise UserError(_(
                'There is not obsolete products to replace'))
        return res

    lines = fields.One2many(
        'replacement.product.line', 'replacement_id', default=_get_lines)

    @api.multi
    def check_active_model(self):
        """
        check that the active model is purchase order.
        if not raise a warning.
        """
        model = self._context.get('active_model', False)
        if model == 'purchase.order':
            pass
        elif model:
            raise UserError(' '.join([
                _('This wizard is not designed to work from the'),
                str(model)]))
        else:
            raise UserError(
                _('This wizard need to be called from a model'))

    @api.multi
    def replacement(self):
        """
        Update the replacement products.
        """
        self.check_active_model()
        order = self._context.get('active_id', False)
        order = self.env['purchase.order'].browse(order)
        for line in self.lines:
            line.line_id.write({'product_id': line.replace_product_id.id})


class ReplacementProductLines(models.TransientModel):

    """
    Let to select a replacement product for every obsolete product.
    """

    _name = 'replacement.product.line'
    _description = 'Select a replacement for every obsolete product'

    replacement_id = fields.Many2one(
        'replacement.product', 'Replacement Wizard')
    obsolete_product_id = fields.Many2one(
        'product.product', 'Obsolete Product',
        domain=[('state2', '=', 'obsolete')])
    replace_product_id = fields.Many2one(
        'product.product', 'Replacement Product',
        domain=[('state2', '!=', 'obsolete')])
    line_id = fields.Many2one('purchase.order.line', 'Purchase Order Line')
    number = fields.Integer(related='line_id.sequence')

    @api.constrains('replace_product_id')
    def _check_replace_product(self):
        """
        replace_product_id must not be an obsolete product.
        """
        if self.replace_product_id and \
                self.replace_product_id.state2 in ['obsolete']:
            raise ValidationError(
                _("The replacement line replace product can not be a"
                  " obsolete product"))

    @api.constrains('obsolete_product_id')
    def _check_obsolete_product(self):
        """
        obsolete_product_id must be an obsolete product.
        """
        if self.obsolete_product_id and \
                self.obsolete_product_id.state2 not in ['obsolete']:
            raise ValidationError(
                _("The replacement line obsolete product must be a"
                  " obsolete product"))
