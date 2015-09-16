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
    replacement_product_ids = fields.Many2many(
        'product.product',
        'discontinued_product_id', 'replacement_product_id',
        string='Replacement Products for Purchase',
        help="When a product is discontinued this list will be the possible"
             " alternative products that could replace it")
    state2 = fields.Selection([
        ('draft', 'In Development'),
        ('sellable', 'Normal'),
        ('end', 'End of Lifecycle'),
        ('obsolete', 'Obsolete')], default='draft', string='State', copy=False)

    @api.multi
    def get_good_replacements(self):
        """
        return the replacemets that are not obsolete and active.
        """
        replacements = [
            product.id for product in self.replacement_product_ids
            if product.state2 not in ['obsolete'] and product.active]
        return replacements
