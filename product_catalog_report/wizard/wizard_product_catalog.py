##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import wizard
import time
import pooler

_lang_form = '''<?xml version="1.0"?>
<form string="Choose catalog preferencies">
    <separator string="Select a printing language " colspan="4"/>
    <field name="report_lang"/>
   <separator string="Select a Product Categories " colspan="4"/>
    <field name="categories" colspan="4" nolabel="1" />

</form>'''



class wiz_productCatalog(wizard.interface):
    def _get_language(self, cr, uid, context):
        lang_obj=pooler.get_pool(cr.dbname).get('res.lang')
        ids=lang_obj.search(cr, uid, [('active', '=', True),])
        langs=lang_obj.browse(cr, uid, ids)
        return [(lang.code, lang.name ) for lang in langs]

    _lang_fields = {
    'report_lang': {'string':'Language', 'type':'selection', 'selection':_get_language,},
    'categories': {'string':'Select Category', 'type':'many2many', 'relation':'product.category', 'required':True},
    }

    def _load(self,cr,uid,data,context):
        partner_obj=pooler.get_pool(cr.dbname).get('res.partner')
        partners=partner_obj.browse(cr, uid, [data['id']])
        if len(partners)>0:
            data['form']['report_lang']=partners[0].lang
        return data['form']
    states = {
        'init': {
            'actions': [_load],
            'result': {'type': 'form', 'arch':_lang_form, 'fields':_lang_fields, 'state':[('end','Cancel'),('print','Print Product Catalog') ]}
        },
        'print': {
            'actions': [],
            'result': {'type': 'print', 'report': 'product_catalog', 'state':'end'}
        }
    }
wiz_productCatalog('res.partner.product_catalog')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

