# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Author: Leonardo Pistone <leonardo.pistone@camptocamp.com>                #
#   Copyright 2013 Camptocamp SA                                              #
#                                                                             #
#   Inspired by the module product_custom_attributes                          #
#   by Benoît GUILLOT <benoit.guillot@akretion.com>, Akretion                 #
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

from openerp.osv import fields, osv
from tools.translate import _
from lxml import etree
import re
import itertools


class stock_production_lot(osv.Model):
    _inherit = "stock.production.lot"

    def _search_all_attributes(self, cr, uid, obj, name, args, context):
        """Search in all serialized attributes

        Receives a domain in args, and expands all relevant terms into ids
        to search into all attributes. The ORM will take care of security
        afterwards, so it' OK to use SQL here.

        In the future, we could consider storing attributes as native
        PostgreSQL hstore or JSON instead of strings, and substitute this rough
        regexp search with native PostgreSQL goodness.

        """

        def expand_serialized(arg):
            """Expand the args in a trivial domain ('id', 'in', ids)"""
            ser_attributes = self.pool['attribute.attribute'].search(
                cr, uid, [
                    ('name', '=', self._name),
                    ('serialized', '=', True),
                ], context=context)

            #  we need this check, otherwise the column x_custom_json_attrs
            #  does not exist in the database. Because of transactions, we
            #  cannot try-pass errors on the database.
            if ser_attributes:
                if arg[1] == 'like':
                    operator = '~'
                elif arg[1] == 'ilike':
                    operator = '~*'
                else:
                    raise osv.except_osv(
                        _('Not Implemented!'),
                        _('Search not supported for this field'))

                cr.execute(
                    """
                        select id
                        from {0}
                        where x_custom_json_attrs {1} %s;
                    """.format(self._table, operator),
                    (ur'.*: "[^"]*%s' % re.escape(arg[2]),)
                )
                sql_ids = [line[0] for line in cr.fetchall()]
                return [('id', 'in', sql_ids)]
            else:
                return [('id', 'in', [])]

        def expand_not_serialized(arg):
            """Expand the args in a domain like
            ['|', ('real_field_1', operator, string),
            ('real_field_2', operator, string)"""
            if arg[1] not in ('like', 'ilike'):
                raise osv.except_osv(
                    _('Not Implemented!'),
                    _('Search not supported for this field'))

            attribute_pool = self.pool.get('attribute.attribute')

            field_ids = attribute_pool.search(cr, uid, [
                ('model_id.model', '=', self._name),
                ('serialized', '=', False)
            ], context=context)
            fields = attribute_pool.browse(cr, uid, field_ids, context=context)
            terms = [(f.name, arg[1], arg[2]) for f in fields]
            return ['|'] * (len(terms) - 1) + terms

        def expand(arg):
            """Expand each argument in a domain we can pass upstream"""
            if isinstance(arg, tuple) and arg[0] == name:
                return ['|'] + expand_serialized(arg) + expand_not_serialized(arg)
            else:
                return [arg]
        return list(itertools.chain.from_iterable(expand(arg) for arg in args))

    _columns = {
        'attribute_set_id': fields.many2one('attribute.set', 'Attribute Set'),
        'attribute_group_ids': fields.related(
            'attribute_set_id',
            'attribute_group_ids',
            type='many2many',
            relation='attribute.group'
            ),
        'search_all_attributes': fields.function(
            lambda self, cr, uid, ids, field, args, context: u'',
            type="char",
            fnct_search=_search_all_attributes,
            method=True,
            string="Search all Attributes"),
    }

    def _fix_size_bug(self, cr, uid, result, context=None):
        """When created a field text dynamicaly, its size is limited to 64 in
        the view. The bug is fixed but not merged
        https://code.launchpad.net/~openerp-dev/openerp-web/6.1-opw-579462-cpa
        To remove when the fix will be merged

        """
        for field in result['fields']:
            if result['fields'][field]['type'] == 'text':
                if 'size' in result['fields'][field]:
                    del result['fields'][field]['size']
        return result

    def open_attributes(self, cr, uid, ids, context=None):
        """Open the attributes of an object

        This method is called when the user presses the Open Attributes button
        in the form view of the object. It opens a dinamically-built form view.

        :param ids: this is normally a singleton. If a longer list is passed,
                    we consider only the first item.

        """

        if context is None:
            context = {}

        model_data_pool = self.pool.get('ir.model.data')

        for lot in self.browse(cr, uid, ids, context=context):
            view_id = model_data_pool.get_object_reference(
                cr, uid,
                'production_lot_custom_attributes',
                'lot_attributes_form_view')[1]
            ctx = {
                'open_attributes': True,
                'attribute_group_ids': [
                    group.id for group in lot.attribute_group_ids
                ]
            }

            return {
                'name': 'Lot Attributes',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [view_id],
                'res_model': self._name,
                'context': ctx,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'res_id': lot.id,
            }

    def save_and_close_lot_attributes(self, cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        """Dinamically adds attributes to the view

        Modifies dinamically the view to show the attributes. If the users
        presses the Open Attributes button, the attributes are shown in a
        new form field. Otherwise, if the attribute set is known beforehand,
        attributes are added to a new tab in the main form view.

        """
        if context is None:
            context = {}
        attr_pool = self.pool.get('attribute.attribute')
        result = super(stock_production_lot, self).fields_view_get(
            cr, uid, view_id, view_type, context, toolbar=toolbar,
            submenu=submenu
        )
        if view_type == 'form' and context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])
            #hide button under the name
            button = eview.xpath("//button[@name='open_attributes']")
            if button:
                button = button[0]
                button.getparent().remove(button)
            attributes_notebook, toupdate_fields = (
                attr_pool._build_attributes_notebook(
                    cr, uid, context['attribute_group_ids'], context=context
                )
            )
            result['fields'].update(
                self.fields_get(cr, uid, toupdate_fields, context)
            )
            if context.get('open_attributes'):
                # i.e. the user pressed the open attributes button on the
                # form view. We put the attributes in a separate form view
                placeholder = eview.xpath(
                    "//separator[@string='attributes_placeholder']"
                )[0]
                placeholder.getparent().replace(
                    placeholder, attributes_notebook
                )
            elif context.get('open_lot_by_attribute_set'):
                # in this case, we know the attribute set beforehand, and we
                # add the attributes to the current view
                main_page = etree.Element(
                    'page', string=_('Custom Attributes')
                )
                main_page.append(attributes_notebook)
                info_page = eview.xpath(
                    "//page[@string='%s']" % (_('Stock Moves'),)
                )[0]
                info_page.addnext(main_page)
            result['arch'] = etree.tostring(eview, pretty_print=True)
            result = self._fix_size_bug(cr, uid, result, context=context)
        return result
