# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#
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
#
##############################################################################
from openerp import models, fields, api, _


class ProductPricelistItem(models.Model):

    _inherit = 'product.pricelist.item'

    def _price_field_get_ext(self):
        result = self._price_field_get()
        result.append((-3, _('Fixed Price')))
        return result

    base_ext = fields.Selection(selection='_price_field_get_ext',
                                string='Based on',
                                size=-1,
                                required=True,
                                default=lambda self:
                                    self.default_get(
                                        fields_list=['base'])['base'],
                                    help="Base price for computation")

    @api.onchange('base_ext')
    def change_base_ext(self):
        base = self.base_ext
        if base == -3:
            base = self._get_default_base(
                {'type': self.price_version_id.pricelist_id.type})
            self.price_discount = -1
        self.base = base
