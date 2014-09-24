# -*- coding: utf-8 -*-


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    def onchange_calculate_volume(self, cr, uid, ids, length, high, width, dimensional_uom_id, context=None):
        v = {}
        if not length or not high or not width or not dimensional_uom_id:
            volume = False
        else:
            dimensional_uom = self.pool.get('product.uom').browse(cr, uid, dimensional_uom_id, context=context)
            length_m = self.get_measure_in_meters(length, dimensional_uom)
            high_m = self.get_measure_in_meters(high, dimensional_uom)
            width_m = self.get_measure_in_meters(width, dimensional_uom)
            if not length_m or not high_m or not width_m:
                volume = False
            else:
                volume = length_m * high_m * width_m
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
        'length': fields.float('Largo'), # Largo
        'high': fields.float('Alto'), # Alto
        'width': fields.float('Ancho'), # Ancho
        'dimensional_uom': fields.many2one('product.uom', 'UdM dimensional',
                                           domain="[('category_id.name', '=', 'Length / Distance')]",
                                           help='Unidad de Medida Dimensional para Largo, Alto y Ancho'),
    }

product_product()









