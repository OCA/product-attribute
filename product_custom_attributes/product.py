# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   product_custom_attributes for OpenERP                                      #
#   Copyright (C) 2011 Akretion Benoît GUILLOT <benoit.guillot@akretion.com>  #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.osv.orm import setup_modifiers
from tools.translate import translate
from lxml import etree

class product_template(Model):
    _inherit = "product.template"

    _columns = {
        'attribute_set_id': fields.many2one('attribute.set', 'Attribute Set'),
    }


class product_product(Model):
    _inherit = "product.product"

    def _attr_grp_ids(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for i in ids:
            set_id = self.read(cr, uid, [i], fields=['attribute_set_id'],
                     context=context)[0]['attribute_set_id']
            if not set_id:
                res[i] = []
            else:
                res[i] = self.pool.get('attribute.group').search(cr, uid,
                      [('attribute_set_id', '=', set_id[0])])
        return res

    _columns = {
        'attribute_group_ids': fields.function(_attr_grp_ids, type='many2many',
        relation='attribute.group', string='Groups')
    }

    def open_attributes(self, cr, uid, ids, context=None):
        ir_model_data_obj = self.pool.get('ir.model.data')
        ir_model_data_id = ir_model_data_obj.search(cr, uid, [['model', '=', 'ir.ui.view'], ['name', '=', 'product_attributes_form_view']], context=context)
        if ir_model_data_id:
            res_id = ir_model_data_obj.read(cr, uid, ir_model_data_id, fields=['res_id'])[0]['res_id']
        grp_ids = self._attr_grp_ids(cr, uid, [ids[0]], [], None, context)[ids[0]]
        ctx = {'open_attributes': True, 'attribute_group_ids': grp_ids}

        return {
            'name': 'Product Attributes',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': self._name,
            'context': ctx,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': ids and ids[0] or False,
        }

    def save_and_close_product_attributes(self, cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}

        def translate_view(source):
            """Return a translation of type view of source."""
            return translate(
                cr, None, 'view', context.get('lang'), source
            ) or source

        result = super(product_product, self).fields_view_get(cr, uid, view_id,view_type,context,toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])
            #hide button under the name
            button = eview.xpath("//button[@name='open_attributes']")
            if button:
                button = button[0]
                button.getparent().remove(button)
            attributes_notebook, toupdate_fields = self.pool.get('attribute.attribute')._build_attributes_notebook(cr, uid, context['attribute_group_ids'], context=context)
            result['fields'].update(self.fields_get(cr, uid, toupdate_fields, context))
            if context.get('open_attributes'):
                placeholder = eview.xpath("//separator[@string='attributes_placeholder']")[0]
                placeholder.getparent().replace(placeholder, attributes_notebook)
            elif context.get('open_product_by_attribute_set'):
                main_page = etree.Element(
                    'page',
                    string=translate_view('Custom Attributes')
                )
                main_page.append(attributes_notebook)
                info_page = eview.xpath(
                    "//page[@string='%s']" % (translate_view('Information'),)
                )[0]
                info_page.addnext(main_page)
            result['arch'] = etree.tostring(eview, pretty_print=True)
        return result
