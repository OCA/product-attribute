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

from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def open_product_pricing(self):
        self.ensure_one()
        action = self.env.ref('product.product_normal_action')
        result = action.read()[0]
        result['context'] = {
            'pricelist': True,
            'search_default_pricelist_id': self.property_product_pricelist.id
        }
        return result
