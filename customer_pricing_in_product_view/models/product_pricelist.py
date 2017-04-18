# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution - module extension
#    Copyright (C) 2014- O4SB (<http://o4sb.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm


class ProductPricelist(orm.Model):
    _inherit = 'product.pricelist'

    def name_get(self, cr, uid, ids, context=None):
        """
        When using widget=selection the orm seems to take care of converting
        the id to a list, but when passing in context (even when passing as
        a list) it converts to an int, causing name_get to fail.  This function
        just converts a single id to a list and passes to super.
        :return: tuple of (id, name)
        """
        if isinstance(ids, int):
            ids = [ids]
        return super(ProductPricelist, self).name_get(cr, uid, ids,
                                                      context=context)
