# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   product_custom_attributes for OpenERP                                     #
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
from openerp import models, fields, api
from tools.translate import translate
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_set_id = fields.Many2one(
        comodel='attribute.set',
        string='Attribute Set')


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.one
    @api.depends()
    def _attr_grp_ids(self):
        set_id = self.attribute_set_id
        if not set_id:
            self.attribute_group_ids = False
        else:
            group_ids = self.env['attribute.group'].search(
                [('attribute_set_id', '=', set_id)])
            self.attribute_group_ids = group_ids

    attribute_group_ids = fields.Many2many(
        comodel='attribute.group',
        string='Groups',
        compute='_attr_grp_ids'
    )

    @api.multi
    def open_attributes(self):
        self.ensure_one()
        form_view = self.env.ref(
            'product_custom_attributes.product_attributes_form_view', False)
        if form_view:
            res_id = form_view.res_id
        grp_ids = self._attr_grp_ids()
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
            'res_id': self.id or False,
        }

    @api.multi
    def save_and_close_product_attributes(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def fields_view_get(
            self, view_id=None,
            view_type='form',
            toolbar=False,
            submenu=False):

        def translate_view(source):
            """Return a translation of type view of source."""
            return translate(
                self._cr, None, 'view', self._context.get('lang'), source
            ) or source

        result = super(ProductProduct, self).fields_view_get(
            view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self._context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])
            button = eview.xpath("//button[@name='open_attributes']")
            if button:
                button = button[0]
                button.getparent().remove(button)
            attributes_notebook, toupdate_fields =\
                self.env['attribute.attribute']._build_attributes_notebook(
                    self._context['attribute_group_ids'])
            result['fields'].update(self.fields_get(toupdate_fields))
            if self._context.get('open_attributes'):
                placeholder = eview.xpath(
                    "//separator[@string='attributes_placeholder']")[0]
                placeholder.getparent().replace(
                    placeholder, attributes_notebook)
            elif self._context.get('open_product_by_attribute_set'):
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
