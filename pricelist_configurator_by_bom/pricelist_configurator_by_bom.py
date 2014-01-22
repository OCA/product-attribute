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
import datetime
import openerp.addons.decimal_precision as dp


class product_pricelist_configurator_line(Model):
    _name = 'product.pricelist.configurator.line'
    _rec_name = 'bom_id'

    _columns = {
        'product_id': fields.related(
            'bom_id', 'product_id', type="many2one",
            relation='product.product', readonly=True, string="Product"),
        'cost_price': fields.related(
            'product_id', 'standard_price', type="float",
            digits_compute=dp.get_precision('Product Price'),
            store=False, readonly=True, string="Cost Price"),
        'margin': fields.float(
            'Margin',
            digits_compute=dp.get_precision('Product Price'),
            required=True),
        'quantity': fields.float(
            'Quantity',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            readonly=True),
        'bom_id': fields.many2one('mrp.bom', 'Bom', readonly=True),
        'configurator_id': fields.many2one(
            'product.pricelist.configurator',
            'Configurator'),
    }


class product_pricelist_configurator(Model):
    _name = 'product.pricelist.configurator'

    def on_change_bom_id(self, cr, uid, ids, bom_id):
        res = {'value': {"line_ids": ''}}
        val = []
        if bom_id:
            bom_obj = self.pool.get('mrp.bom').browse(cr, uid, bom_id)
            for line in bom_obj.bom_lines:
                val.append({
                    'product_id': line.product_id.id,
                    'cost_price': line.product_id.standard_price,
                    'bom_id': line.id,
                    'quantity': line.product_qty})
        res['value']['line_ids'] = val
        return res

    def on_change_product_id(self, cr, uid, ids, product_id):
        res = {'value': {"bom_id": ''}}
        bom_ids = self.pool.get('mrp.bom').search(
            cr, uid, [('product_id', '=', product_id)])
        if bom_ids:
            res['value']['bom_id'] = bom_ids[0]
        return res

    def compute_final_price(self, cr, uid, ids, context=None):
        val = 0
        for conf in self.browse(cr, uid, ids):
            if conf.line_ids:
                for l in conf.line_ids:
                    if l.margin != 0:
                        val = val + l.cost_price * l.margin * l.quantity
                    else:
                        val = val + l.cost_price * l.quantity
                self.pool.get('product.pricelist.configurator').write(
                    cr, uid, conf.id, {'amount': val}, context=context)
        return True

    def create_pricelist_item(self, cr, uid, ids, context=None):
        for conf in self.browse(cr, uid, ids):
            pricelist_id = conf.partner_id.property_product_pricelist
            pricelist_version_ids = self.pool.get(
                'product.pricelist.version').search(
                cr, uid, [(
                    'pricelist_id', 'in', [pricelist_id.id]),
                    '|',
                    ('date_start', '=', False),
                    ('date_start', '<=', datetime.datetime.today()),
                    '|',
                    ('date_end', '=', False),
                    ('date_end', '>=', datetime.datetime.today()),
                    ])
            #One active version at time
            if not pricelist_version_ids:
                raise osv.except_osv(('Warning!'), (
                    """At least one pricelist has no active version
                    !\nPlease create or activate one."""))
            else:
                for price in self.pool.get(
                    'product.pricelist.version').browse(
                        cr, uid, pricelist_version_ids):
                    for item in price.items_id:
                        if item.product_id == conf.product_id:
                            raise osv.except_osv(('Warning!'), (
                                """A pricelist item already existing
                                for product %s and partner %s.""" % (
                                conf.product_id.name,
                                conf.partner_id.name)))
                    val = {
                        'price_version_id': price.id,
                        'product_id': conf.product_id.id,
                        'price_discount': -1,
                        'price_surcharge': conf.amount,
                        'name':
                        str(conf.product_id.name)
                        + "-" +
                        str(conf.partner_id.name)}
                    pricelist_id = self.pool.get(
                        'product.pricelist.item').create(cr, uid, val)
                    conf.write({'pricelist_item_id': pricelist_id})
        return True

    def write_pricelist_item(self, cr, uid, ids, context=None):
        for conf in self.browse(cr, uid, ids):
            if conf.pricelist_item_id:
                self.pool.get('product.pricelist.item').write(
                    cr, uid, conf.pricelist_item_id.id,
                    {'price_surcharge': conf.amount}, context=context)
        return True

    _columns = {
        'product_id': fields.many2one(
            'product.product', 'Product', required=True),
        'partner_id': fields.many2one(
            'res.partner', 'Partner', required=True),
        'line_ids': fields.one2many(
            'product.pricelist.configurator.line',
            'configurator_id', string='Line'),
        'amount': fields.float(
            'Amount',
            digits_compute=dp.get_precision('Product Price'),
            readonly=True),
        'pricelist_item_id': fields.many2one(
            'product.pricelist.item', 'Pricelist'),
        'bom_id': fields.many2one('mrp.bom', 'Bom'),
    }
