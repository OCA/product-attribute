# -*- encoding: utf-8 -*-
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


class ReplacementProduct(models.TransientModel):

    """
    Wizard that let to select one of the replacement product of a discontinued
    product.
    """

    _name = 'replacement.product'
    _description = ('Replacement of discontinued products'
                    ' for purchase operations')

    @api.multi
    def _get_lines(self):
        """
        Get the lines with discontinued products

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
                'discontinued_product_id': line.product_id.id,
                'replacement_product_ids':
                    line.product_id.replacement_product_ids,
            })
            for line in order.order_line
            if line.product_id.state2 in ['obsolete']]
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
            raise exceptions.Warning(' '.join([
                _('This wizard is not designed to work from the'),
                str(model)]))
        else:
            raise exceptions.Warning(
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
            line.line_id.write({
                'product_id': line.replacement_product_id.id,
                'discontinued_product_id': line.discontinued_product_id.id
            })


class ReplacementProductLines(models.TransientModel):

    """
    Let to select a replacement product for every discontinued product.
    """

    _name = 'replacement.product.line'
    _description = 'Select a replacement for every discontinued product'

    replacement_id = fields.Many2one(
        'replacement.product', 'Replacement Wizard')
    discontinued_product_id = fields.Many2one(
        'product.product', 'Discontinued Product',
        domain=[('state2', '=', 'obsolete')])
    replacement_product_ids = fields.Many2many(
        related="discontinued_product_id.replacement_product_ids")
    replacement_product_id = fields.Many2one(
        'product.product', 'Replacement Product for Purchase')
    line_id = fields.Many2one('purchase.order.line', 'Purchase Order Line')
    number = fields.Integer(related='line_id.sequence')

    @api.onchange('discontinued_product_id')
    def get_replacement_product_ids(self):
        """
        Return the list of replacement products
        @return domain
        """
        self.replacement_product_id = False
        res = {'domain': {'replacement_product_id': [('id', 'in', [])]}}
        replacement_ids = self.discontinued_product_id.get_good_replacements()
        if replacement_ids:
            if len(replacement_ids) == 1:
                self.replacement_product_id = replacement_ids[0]
            res = {'domain': {
                'replacement_product_id': [('id', 'in', replacement_ids)]}}
        return res

    @api.one
    @api.constrains('replacement_product_id', 'discontinued_product_id')
    def _check_line(self):
        """
        This method will check that when creating the replacement line the
        replacement_product_id and the discontinued_product_id belongs to the
        correspond states.
            - discontinued_product_id must be an obsolete product.
            - replacement_product_id must not be an obsolete product.
        """
        if self.replacement_product_id and \
                self.replacement_product_id.state2 in ['obsolete']:
            raise exceptions.ValidationError(
                _("The Replacement product can not be a obsolete product"))
        if self.discontinued_product_id and \
                self.discontinued_product_id.state2 not in ['obsolete']:
            raise exceptions.ValidationError(
                _("The Discontinued producr must be a obsolete product"))
