# -*- coding: utf-8 -*-
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    Copyright 2015 Camptocamp SA
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


from openerp import models, fields
from openerp.api import multi


class Product(models.Model):
    _inherit = 'product.product'

    @multi
    def compute_volume(self, length, heigth, width, dimensional_uom_id):
        if not length or not heigth or not width or not dimensional_uom_id:
            return False
        else:
            dimensional_uom = self.env['product.uom'].browse(
                dimensional_uom_id)
            length_m = self.convert_to_meters(length, dimensional_uom)
            heigth_m = self.convert_to_meters(heigth, dimensional_uom)
            width_m = self.convert_to_meters(width, dimensional_uom)
            return length_m * heigth_m * width_m

    @multi
    def onchange_calculate_volume(self, length, heigth, width,
                                  dimensional_uom_id):
        return {'value':
                {'volume': self.compute_volume(length, heigth, width,
                                               dimensional_uom_id)}
                }

    def convert_to_meters(self, measure, dimensional_uom):
        UOM = self.env['product.uom']
        uom_meters = UOM.search([('name', '=', 'm')])
        return UOM._compute_qty_obj(from_unit=dimensional_uom,
                                    qty=measure,
                                    to_unit=uom_meters)

    length = fields.Float()
    heigth = fields.Float(oldname='high')
    width = fields.Float()
    dimensional_uom = fields.Many2one(
        'product.uom',
        'Dimensional UoM',
        domain="[('category_id.name', '=', 'Length / Distance')]",
        help='UoM for length, heigth, width')
