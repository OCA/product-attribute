# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp.osv import osv
from openerp.osv import fields


class Product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def onchange_calculate_volume(self, cr, uid, ids, length, heigth, width,
                                  dimensional_uom_id, context=None):
        v = {}
        if not length or not heigth or not width or not dimensional_uom_id:
            volume = False
        else:
            dimensional_uom = self.pool.get('product.uom').browse(
                cr, uid, dimensional_uom_id, context=context)
            length_m = self.get_measure_in_meters(length, dimensional_uom)
            heigth_m = self.get_measure_in_meters(heigth, dimensional_uom)
            width_m = self.get_measure_in_meters(width, dimensional_uom)
            if not length_m or not heigth_m or not width_m:
                volume = False
            else:
                volume = length_m * heigth_m * width_m
        v['volume'] = volume
        return {'value': v}

    def get_measure_in_meters(self, measure, dimensional_uom):
        if not dimensional_uom:
            return None

        measure = float(measure)
        if dimensional_uom.name == 'm':
            return measure
        elif dimensional_uom.name == 'km':
            return measure * 1000
        elif dimensional_uom.name == 'cm':
            return measure / 100
        else:
            return None

    _columns = {
        'length': fields.float('Length'),
        'heigth': fields.float('Heigth', oldname='high'),
        'width': fields.float('Width'),
        'dimensional_uom': fields.many2one(
            'product.uom',
            'UdM dimensional',
            domain="[('category_id.name', '=', 'Length / Distance')]",
            help='UoM for length, heigth, width'),
    }
