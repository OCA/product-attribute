# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: David BEAL
#    Copyright 2015 Akretion
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

from openerp import models, fields, api
from openerp.exceptions import Warning
from lxml import etree


# These fields must not be synchronized between product.profile
# and product.template
PROFILE_FIELDS_TO_EXCLUDE = ['name', 'description', 'sequence',
                             'display_name', '__last_update']


def format_except_message(error, field, self):
    value = self.profile_id[field]
    model = type(self)._name
    message = ("Issue:\n%s\n'%s' value can't be applied to '%s' field."
               "\nThere is no matching value between 'Product Profiles' "
               "\nand '%s' models for this field.\n\nResolution:\n"
               "Check your settings on Profile model:\n"
               "Sales > Configuration > Product Categories and Attributes"
               "> Product Profiles"
               % (error, value, field, model))
    return message


class ProductProfile(models.Model):
    _name = 'product.profile'
    _order = 'sequence'

    def _get_types(self):
        """ inherit in your custom module.
            could be this if stock module is installed

        return [('product', 'Stockable Product'),
                ('consu', 'Consumable'),
                ('service', 'Service')]
        """
        return [('consu', 'Consumable'), ('service', 'Service')]

    name = fields.Char(
        required=True,
        help="Profile name displayed on product template\n"
             "(not synchronized with product.template fields)")
    sequence = fields.Integer(
        help="Allows to define the order of the entries of profile_id field\n"
             "(not synchronized with product.template fields)")
    description = fields.Text(
        required=True,
        help="Allows to display an explanation on the selected profile\n"
             "(not synchronized with product.template fields)")
    type = fields.Selection(
        selection='_get_types',
        required=True,
        help="see 'type' field in product.template")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    profile_id = fields.Many2one(
        'product.profile',
        string='Profile')
    profile_description = fields.Text(
        related='profile_id.description',
        string='Profile explanation',
        readonly=True)

    @api.model
    def _fields_to_populate(self, profile):
        fields_to_exclude = PROFILE_FIELDS_TO_EXCLUDE
        fields_to_exclude.extend(models.MAGIC_COLUMNS)
        return [field for field in profile._fields.keys()
                if field not in fields_to_exclude]

    @api.onchange('profile_id')
    def _onchange_from_profile(self, vals=None):
        """ Update product fields with product.profile corresponding fields """
        # TODO CLEAN
        defaults = {}
        to_play = False
        profile = None
        if vals and vals.get('profile_id'):
            # in case of creation by script
            to_play = True
            profile = self.env['product.profile'].search(
                [('id', '=', vals['profile_id'])])
        for field in self._fields_to_populate(self.profile_id):
            if self.profile_id:
                try:
                    self[field] = self.profile_id[field]
                    print '     prof', field
                except ValueError as e:
                    raise Warning(format_except_message(e, field, self))
                except Exception as e:
                    raise Warning("%s" % e)
            elif to_play:
                defaults.update({field: profile[field]})
                print '    defaults', field
            else:
                # also on field initialisation
                self[field] = False
                print '     false', field
        return defaults

    @api.model
    def create(self, vals):
        if vals.get('profile_id'):
            defaults = self._onchange_from_profile(vals)
            vals = dict(defaults, **vals)
        return super(ProductTemplate, self).create(vals)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """ WIP """
        res = super(ProductTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            fields = self._fields_to_populate(self.profile_id)
            for field in fields:
                xml = doc.xpath("//field[@name='%s']" % field)[0]
                attrs = xml.attrib
                if 'attrs' in attrs:
                    print ''
                else:
                    xml.attrib['attrs'] = '{\'invisible\': True}'
                    # print xml[0].attrib['modifiers']
            res['arch'] = etree.tostring(doc, pretty_print=True)
            print res['arch']
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('profile_id')
    def _onchange_from_profile(self, vals=None):
        """ Update product fields with product.profile corresponding fields
            WIP
        """
        if isinstance(self.id, models.NewId):
            print 'PROFILE_ID', self.profile_id
            if self.profile_id:
                if not isinstance(vals, dict):
                    vals = {}
                vals['profile_id'] = self.profile_id.id
                print '     YES  pppppp'
                return self.product_tmpl_id._onchange_from_profile(
                    vals=vals)
        else:
            return self.product_tmpl_id._onchange_from_profile(vals=vals)
