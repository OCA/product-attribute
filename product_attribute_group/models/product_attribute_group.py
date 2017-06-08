# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP / Odoo, Open Source Management Solution - module extension
#    Copyright (C) 2015- O4SB (<http://openforsmallbusiness.co.nz>).
#    Author Graeme Gellatly <g@o4sb.com>
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

from openerp import api, fields, models, _
from openerp import exceptions


class ProductAttributeGroup(models.Model):
    """Product Attribute Group"""
    _name = 'product.attribute.group'
    _description = __doc__
    _order = 'name'

    name = fields.Char(required=True)

    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Product Attribute',
        required=True,)

    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        # default relation name exceed postgres limit of 63 characters
        # causing conflict with index see:
        # https://github.com/odoo/odoo/issues/2780
        relation='attr_group_attr_value_rel',
        string='Attribute Values')

    attribute_line_ids = fields.Many2many(
        comodel_name='product.attribute.line',
        relation='attr_group_attr_line_rel',
        string='Attribute Lines',
        )

    _sql_constraints = [(
        'uniq_name_attribute_id',
        'unique(name,attribute_id)',
        'The name of the group must be unique for an attribute'
    )]

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = self.name + ' (Copy)'
        default['attribute_line_ids'] = False
        return super(ProductAttributeGroup, self).copy(default=default)

    @api.multi
    def unlink(self):
        for record in self:
            if record.attribute_line_ids:
                raise exceptions.except_orm(
                    'PROHIBITED',
                    'Cannot delete attribute group while still assigned '
                    'to products')
        return super(ProductAttributeGroup, self).unlink()

    @api.one
    def action_update_variants(self):
        for line in self.attribute_line_ids:
            line._onchange_attribute_group_ids()
            line.product_tmpl_id.create_variant_ids()

    @api.onchange('attribute_value_ids')
    def _onchange_attribute_value_ids(self):
        """
        In order to ensure consistency across products changing an attribute
        group requires updating all existing variants.  While this warning
        will pop every time a user adds a value to an existing attribute
        group, it is better than having to wait for variants to be recreated
        every time
        :return: If there are existing products a warning message.
        """
        if self.attribute_line_ids:
            return {'warning': {'title': _('PLEASE NOTE:'),
                                'message': _('You must click Update Variants '
                                             'after saving in order to update '
                                             'existing variants.  If you do '
                                             'not want to do this, you should '
                                             'discard changes and create a '
                                             'new attribute group')}}

    @api.onchange('attribute_id')
    def _onchange_attribute_id(self):
        """
        Ensures that attribute types cannot be changed if already
        assigned to a template.
        :return: void
        """
        if self.attribute_line_ids:
            raise exceptions.except_orm(
                _('PROHIBITED:'), _('You cannot change the attribute '
                                    'type of a group already '
                                    'assigned to a template'))
        if self.attribute_value_ids:
            self.attribute_value_ids = self.env['product.attribute.value']

    @api.one
    @api.constrains('attribute_id')
    def _check_attribute_id(self):
        msg = ('PROHIBITED: You cannot change the attribute '
               'type of a group already assigned to a template')
        for attr_value in self.attribute_value_ids:
            if attr_value.attribute_id != self.attribute_id:
                raise exceptions.ValidationError(msg)
        for line in self.attribute_line_ids:
            if line.attribute_id != self.attribute_id:
                raise exceptions.ValidationError(msg)


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    attribute_group_ids = fields.Many2many(
        comodel_name='product.attribute.group',
        relation='attr_group_attr_line_rel',
        string='Attribute Groups')

    # Because users may manually add attributes outside of the group
    # we must manually keep track of thos additions
    manually_added_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='attr_value_attr_line_manual_rel',
        string='Manually Added Values')

    @api.onchange('value_ids')
    def _onchange_value_ids(self):
        """
        When attribute values are manually added or removed they are
        reflected in manually added_ids.  This allows a small degree of
        customization.  However removing attribute values belonging to
        an assigned attribute group is discouraged and raises a warning.
        @note: This function "should" raise an error and repopulate
            the value_ids. However updating a self referenced field of
            an x2many relation is not supported by the ORM.  See
             https://github.com/odoo/odoo/issues/2693.
        :return: Warning in case of removing attribute value from group
        """
        self.temp_value_ids = self.env['product.attribute.value']
        auto_values = self.env['product.attribute.value']
        for group in self.attribute_group_ids:
            auto_values = auto_values | group.attribute_value_ids
        self.manually_added_value_ids = self.value_ids - auto_values
        if (len(self.manually_added_value_ids + auto_values) >
                len(self.value_ids)):
            return {'warning': {'title': _('ERROR:'),
                                'message': _(
                                    'You have removed an item belonging '
                                    'to an attribute group.  This will be '
                                    'automatically readded whenever the '
                                    'attribute group is updated, or the '
                                    'attribute groups belonging to the line.')}
                    }

    @staticmethod
    def _attribute_sort_key(value):
        """
        Simple sorting function, abstracted to ease overide. By default
        causes sorted to sort by attribute value name ascending
        :param value:
        :return: string (value.name)
        """
        return value.name

    @api.onchange('attribute_group_ids')
    def _onchange_attribute_group_ids(self):
        """
        :return: The union of existing manually added
            attribute values and values within the
            selected attribute groups
        """
        values = self.manually_added_value_ids
        for group in self.attribute_group_ids:
            values = values | group.attribute_value_ids
        self.value_ids = values.sorted(key=self._attribute_sort_key)


class ProductAttributeValue(models.Model):
    """Inherit Product Attribute Value to add groups"""
    _inherit = 'product.attribute.value'

    attribute_group_ids = fields.Many2many(
        comodel_name='product.attribute.group',
        relation='attr_group_attr_value_rel',
        string='Attribute Groups',
        )

    manual_line_ids = fields.Many2many(
        comodel_name='product.attribute.line',
        relation='attr_value_attr_line_manual_rel',
        string='Manual Product Attribute Lines')


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    attribute_group_ids = fields.One2many(
        comodel_name='product.attribute.group',
        inverse_name='attribute_id',
        string='Attribute Groups')
