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
from openerp import api


class Product(models.Model):
    _inherit = 'product.product'

    @api.onchange('length', 'height', 'width', 'dimensional_uom_id')
    def onchange_calculate_volume(self):
        if (not self.length or not self.height or not self.width
                or not self.dimensional_uom_id):
            return False

        length_m = self.convert_to_meters(self.length, self.dimensional_uom_id)
        height_m = self.convert_to_meters(self.height, self.dimensional_uom_id)
        width_m = self.convert_to_meters(self.width, self.dimensional_uom_id)
        self.volume = length_m * height_m * width_m

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env['product.uom'].search([('name', '=', 'm')])

        return self.env['product.uom']._compute_qty_obj(
            from_unit=dimensional_uom,
            qty=measure,
            to_unit=uom_meters)

    length = fields.Float()
    height = fields.Float(oldname='high')
    width = fields.Float()
    dimensional_uom_id = fields.Many2one(
        'product.uom',
        'Dimensional UoM',
        domain="[('category_id.name', '=', 'Length / Distance')]",
        help='UoM for length, height, width')
