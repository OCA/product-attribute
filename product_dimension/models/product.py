# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


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
