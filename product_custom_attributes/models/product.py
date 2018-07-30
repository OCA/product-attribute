# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   base_attribute.attributes for OpenERP                                     #
#   Copyright (C) 2015 Odoo Community Association (OCA)                       #
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

from odoo import models, fields, api
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = "product.template"

    attribute_set_id = fields.Many2one('attribute.set', 'Attribute Set')

    attribute_group_ids = fields.One2many(
        comodel_name='attribute.group',
        inverse_name='attribute_set_id',
        related='attribute_set_id.attribute_group_ids',
        string='Groups',
        store=False,
    )

    @api.model
    def create(self, vals):
        if not vals.get('attribute_set_id') and vals.get('categ_id'):
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['attribute_set_id'] = category.attribute_set_id.id
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if not vals.get('attribute_set_id') and vals.get('categ_id'):
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['attribute_set_id'] = category.attribute_set_id.id
        super(ProductTemplate, self).write(vals)
        return True

    @api.multi
    def open_attributes(self):
        self.ensure_one()

        view = self.env.ref(
            'product_custom_attributes.product_attributes_form_view')

        grp_ids = self.attribute_group_ids.ids
        ctx = {'open_attributes': True, 'attribute_group_ids': grp_ids}

        return {
            'name': 'Product Attributes',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': self._name,
            'context': ctx,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'res_id': self.id,
        }

    @api.multi
    def save_and_close_product_attributes(self):
        return True

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        context = self.env.context

        result = super(ProductTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)

        if view_type == 'form' and context.get('attribute_group_ids'):
            eview = etree.fromstring(result['arch'])

            # hide button under the name
            button = eview.xpath("//button[@name='open_attributes']")

            if button:
                button = button[0]
                button.getparent().remove(button)

            attributes_notebook, toupdate_fields = (
                self.env['attribute.attribute']._build_attributes_notebook(
                    context['attribute_group_ids']))
            result['fields'].update(self.fields_get(toupdate_fields))

            if context.get('open_attributes'):
                placeholder = eview.xpath(
                    "//separator[@string='attributes_placeholder']")[0]
                placeholder.getparent().replace(
                    placeholder, attributes_notebook)

            elif context.get('open_product_by_attribute_set'):
                notebook = eview.xpath(
                    "//notebook")[0]
                page = etree.SubElement(
                    notebook, 'page', name="attributes_page",
                    colspan="2", col="4", string="Custom attributes")
                page.append(attributes_notebook)

            result['arch'] = etree.tostring(eview, pretty_print=True)
        return result
