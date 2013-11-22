# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Author: Nicola Malcontenti <nicola.malcontenti@agilebg.com>
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
from openerp.osv.orm import Model
from openerp.osv import fields, osv

class product_pricelist_configurator_line(Model):
    _name = 'product.pricelist.configurator.line'

    _columns = {
        'product_id': fields.related('bom_id','product_id',type="many2one",relation='product.product',readonly=True, string="Product"),
		'cost_price': fields.related('product_id', 'standard_price', type="float", store=False, readonly=True, string="Price"),
		'margin': fields.float('Margin',required=True),
		'quantity': fields.float('Description',readonly=True),
		'bom_id': fields.many2one('mrp.bom','Bom',readonly=True),
    }


class product_pricelist_configurator(Model):
    _name = 'product.pricelist.configurator'

    def on_change_bom_id(self, cr, uid, ids, bom_id):
        res = {'value': {"line_ids": ''}}
        val=[]
        if bom_id:
        	bom_obj=self.pool.get('mrp.bom').browse(cr, uid, bom_id)
        	for line in bom_obj.bom_lines:
        		val.append({'product_id':bom_obj.product_id.id, 'cost_price':bom_obj.product_id.standard_price,'bom_id':bom_obj.id,'quantity':bom_obj.product_qty})      
        res['value']['line_ids']=val
        return res

    def on_change_product_id(self, cr, uid, ids, product_id):
    	res = {'value': {"bom_id": ''}}
    	bom_ids=self.pool.get('mrp.bom').search(cr,uid,[('product_id','=',product_id)])
        if bom_ids:
            res['value']['bom_id']=bom_ids[0]
    	return res

    def compute_final_price(self, cr, uid, ids, context=None):
        for conf in self.browse(cr, uid, ids):
            if conf.line_ids:
                for l in conf.line_ids:
                    self.pool.get('product.pricelist.configurator.line').write(cr, uid, l.id, {'amount':l.cost_price*l.margin}, context=context)
        return True

    def create_pricelist_item(self, cr, uid, ids, context=None):


        return True    

    def write_pricelist_item(self, cr, uid, ids, context=None):
        raise osv.except_osv(('alert'), (' Your message'))
        for conf in self.browse(cr, uid, ids):
            if conf.pricelist_item_id:
                self.pool.get('product.pricelist.item').write(cr, uid, conf.pricelist_item_id.id, {'price_surcharge':conf.amount}, context=context)
        return True

    _columns = {
        'product_id': fields.many2one('product.product','Product',required=True),
        'partner_id': fields.many2one('res.partner','Partner',required=True),
		'line_ids': fields.one2many('product.pricelist.configurator.line', 'product_id', string='Line'),
		'amount': fields.float('Amount',readonly=True),
		'pricelist_item_id': fields.many2one('product.pricelist.item','Pricelist'),
		'bom_id': fields.many2one('mrp.bom','Bom'),
    }
