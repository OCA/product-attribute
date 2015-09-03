# coding: utf-8
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

from openerp import models, fields, api, _
from openerp.osv import orm
from openerp.exceptions import Warning
from lxml import etree


PROFILE_MENU = (_("Sales > Configuration \n> Product Categories and Attributes"
                  "\n> Product Profiles"))


def format_except_message(error, field, self):
    value = self.profile_id[field]
    model = type(self)._name
    message = (_("Issue\n------\n"
                 "%s\n'%s' value can't be applied to '%s' field."
                 "\nThere is no matching value between 'Product Profiles' "
                 "\nand '%s' models for this field.\n\n"
                 "Resolution\n----------\n"
                 "Check your settings on Profile model:\n%s"
               % (error, value, field, model, PROFILE_MENU)))
    return message


class ProductProfile(models.Model):
    _name = 'product.profile'
    _order = 'sequence'

    def _get_types(self):
        """ inherit in your custom module.
            could be this one if stock module is installed

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
    explanation = fields.Text(
        required=True,
        oldname='description',
        help="Allows to display an explanation on the selected profile\n"
             "(not synchronized with product.template fields)")
    type = fields.Selection(
        selection='_get_types',
        required=True,
        help="see 'type' field in product.template")


class ProductMixinProfile(models.AbstractModel):
    _name = 'product.mixin.profile'

    @api.model
    def _get_profile_fields_to_exclude(self):
        # These fields must not be synchronized between product.profile
        # and product.template
        return models.MAGIC_COLUMNS + [
            'name', 'explanation', 'sequence',
            'display_name', '__last_update']

    @api.model
    def _get_profile_fields(self):
        fields_to_exclude = set(self._get_profile_fields_to_exclude())
        return [field for field in self.env['product.profile']._fields.keys()
                if field not in fields_to_exclude]

    @api.model
    def _get_profile_data(self, profile_id):
        fields = self._get_profile_fields()
        if profile_id:
            profile = self.env['product.profile']\
                .browse(profile_id).read(fields)[0]
            profile.pop('id')
            return profile
        else:
            return { field: None for field in fields }

    @api.onchange('profile_id')
    def _onchange_from_profile(self):
        """ Update product fields with product.profile corresponding fields """
        for field, value in self._get_profile_data(self.profile_id.id).items():
            try:
                self[field] = self.profile_id[field]
            except ValueError as e:
                raise Warning(format_except_message(e, field, self))
            except Exception as e:
                raise Warning("%s" % e)

    @api.model
    def create(self, vals):
        if vals.get('profile_id'):
            vals.update(self._get_profile_data(vals['profile_id']))
        return super(ProductMixinProfile, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('profile_id'):
            vals.update(self._get_profile_data(vals['profile_id']))
        return super(ProductMixinProfile, self).write(vals)

    @api.model
    def _get_profiles_to_filter(self):
        """ Inherit if you want that some profiles doesn't have a filter """
        return [(x.id, x.name) for x in self.env['product.profile'].search([])]

    @api.model
    def _customize_profile_filters(self, my_filter):
        """ Inherit if you to customize search filter display"""
        return {
            'string': "%s" % my_filter[1],
            'help': 'Filtering by Product Profile',
            'domain': "[('profile_id','=', %s)]" % my_filter[0]}

    @api.model
    def _customize_view(self, res, view_type):
        profile_group = self.env.ref('product_profile.group_product_profile')
        users_in_profile_group = [user.id for user in profile_group.users]
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            fields = self._get_profile_fields()
            fields_def = self.fields_get(allfields=fields)
            if self.env.uid not in users_in_profile_group:
                attrs = {'invisible': [('profile_id', '!=', False)]}
            else:
                attrs = {'readonly': [('profile_id', '!=', False)]}
            paths = ["//field[@name='%s']",
                     "//label[@for='%s']"]
            for field in fields:
                for path in paths:
                    node = doc.xpath(path % field)
                    if node:
                        for current_node in node:
                            current_node.set('attrs', str(attrs))
                            orm.setup_modifiers(current_node,
                                                fields_def[field])
            res['arch'] = etree.tostring(doc, pretty_print=True)
        elif view_type == 'search':
            # Allow to dynamically create search filters for each profile
            filters_to_create = self._get_profiles_to_filter()
            doc = etree.XML(res['arch'])
            node = doc.xpath("//filter[1]")
            if not node:
                return res
            for my_filter in filters_to_create:
                elm = etree.Element(
                    'filter', **self._customize_profile_filters(my_filter))
                node[0].addprevious(elm)
            res['arch'] = etree.tostring(doc, pretty_print=True)
        return res


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'product.mixin.profile']
    _name = 'product.template'

    profile_id = fields.Many2one(
        'product.profile',
        string='Profile')
    profile_explanation = fields.Text(
        related='profile_id.explanation',
        string='Profile Explanation',
        readonly=True)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        """ fields_view_get comes from Model (not AbstractModel)
        """
        res = super(ProductTemplate, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        return self._customize_view(res, view_type)


class ProductProduct(models.Model):
    _inherit = ['product.product', 'product.mixin.profile']
    _name = 'product.product'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        return self._customize_view(res, view_type)
