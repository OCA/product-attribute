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

from openerp import models, fields, api


class ProductProduct(models.Model):

    _inherit = 'product.product'
    replace_to_product_id = fields.One2many(
        'product.product',
        'replaced_by_product_id',
        string='Replace To',
        help="Informative field. The product that is replaced by the"
             " current one. The current product is the new product for"
             " the product in this field")

    replaced_by_product_id = fields.Many2one(
        'product.product',
        string='Replaced By',
        help="The replacement product for the current product."
             " The current product is a obsolete product and the product"
             " in this field is the new product that make the replacement")

    state2 = fields.Selection([
        ('draft', 'In Development'),
        ('sellable', 'Normal'),
        ('end', 'End of Lifecycle'),
        ('obsolete', 'Obsolete')], default='draft', string='State', copy=False)

    @api.multi
    def get_good_replacements(self):
        """:return: the replace by product (new product) if the product is not
                 obsolete and is and active product.
        """
        replace = self.replaced_by_product_id.filtered(
            lambda product: product.state2 not in ['obsolete'] and
            product.active)
        return replace

    @api.multi
    def write(self, values):
        """ Try to set the state2 to obsolete when quantity on hand will change
        the product to end instead.
        """
        for product in self:
            state2 = values.get('state2', product.state2)
            available = (
                values.get('qty_available', product.qty_available) or
                values.get('purchase_incoming_qty',
                           product.purchase_incoming_qty))

            if state2 == 'obsolete' and available:
                values.update({'state2': 'end'})
            elif state2 == 'end' and not available:
                values.update({'state2': 'obsolete'})
            super(ProductProduct, product).write(values)
        return True

    @api.cr_uid
    def update_product_state(self, cr, uid):
        """ Check the product state
            - if in end state but has not inventory then pass to obsolete.
            - if obsolete but with inventory pass to end of life.
        """
        products = self.search(cr, uid, [])
        products = self.browse(cr, uid, products)

        end_product = products.search([]).filtered(
            lambda product: product.state2 == 'obsolete' and (
                product.qty_available or product.purchase_incoming_qty))

        obsolete_product = products.search([]).filtered(
            lambda product: product.state2 == 'end' and not (
                product.qty_available or product.purchase_incoming_qty))

        end_product.write({'state2': 'end'})
        obsolete_product.write({'state2': 'obsolete'})
