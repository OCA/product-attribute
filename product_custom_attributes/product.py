# -*- coding: utf-8 -*-
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import translate
from lxml import etree


class ProductTemplate(Model):
    _inherit = "product.template"

    def _attr_grp_ids(self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for i in ids:
            set_id = self.read(cr, uid, [i], fields=['attribute_set_id'],
                               context=context)[0]['attribute_set_id']
            if not set_id:
                res[i] = []
            else:
                att_group_obj = self.pool['attribute.group']
                res[i] = att_group_obj.search(cr, uid, [('attribute_set_id',
                                                         '=', set_id[0])],
                                              context=context)
        return res

    _columns = {
        'attribute_set_id': fields.many2one('attribute.set', 'Attribute Set'),
        'attribute_group_ids': fields.function(_attr_grp_ids, type='many2many',
                                               relation='attribute.group',
                                               string='Groups')
    }

    def open_attributes(self, cr, uid, ids, context=None):
        ir_mdata_obj = self.pool['ir.model.data']
        ir_mdata_id = ir_mdata_obj.search(cr, uid,
                                          [('model', '=', 'ir.ui.view'),
                                           ('name', '=',
                                            'product_attributes_form_view')],
                                          context=context)
        if ir_mdata_id:
            res_id = ir_mdata_obj.read(cr, uid, ir_mdata_id,
                                       fields=['res_id'])[0]['res_id']
        grp_ids = self._attr_grp_ids(cr, uid, [ids[0]], [], None,
                                     context)[ids[0]]
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

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}

        def translate_view(source):
            """Return a translation of type view of source."""
            return translate(
                cr, None, 'view', context.get('lang'), source
            ) or source

        result = super(ProductTemplate, self).fields_view_get(cr, uid, view_id,
                                                              view_type,
                                                              context,
                                                              toolbar=toolbar,
                                                              submenu=submenu)
        if view_type == 'form' and context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])
            # hide button under the name
            button = eview.xpath("//button[@name='open_attributes']")
            if button:
                button = button[0]
                button.getparent().remove(button)
            attributes_notebook, toupdate_fields = self.pool.\
                get('attribute.attribute').\
                _build_attributes_notebook(cr, uid,
                                           context['attribute_group_ids'],
                                           context=context)
            result['fields'].update(self.fields_get(cr, uid, toupdate_fields,
                                                    context))
            if context.get('open_attributes'):
                placeholder = eview.xpath(
                    "//separator[@string='attributes_placeholder']")[0]
                placeholder.getparent().replace(placeholder,
                                                attributes_notebook)
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
