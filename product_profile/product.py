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


# these fields must not be synchronized between product.profile
# and product.template
PROFILE_FIELDS_TO_EXCLUDE = ['name', 'description', 'sequence',
                             'display_name', '__last_update']


class ProductProfile(models.Model):
    _name = 'product.profile'
    _order = 'sequence ASC'

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
        fields_to_exclude = PROFILE_FIELDS_TO_EXCLUDE
        fields_to_exclude.extend(models.MAGIC_COLUMNS)
        profile_fields = [field for field in self.profile_id._fields.keys()
                          if field not in fields_to_exclude]
        for elm in profile_fields:
            print elm
            if self.profile_id:
                self[elm] = self.profile_id[elm]
            elif to_play:
                defaults.update({elm: profile[elm]})
            else:
                self[elm] = False
        return defaults

    @api.model
    def create(self, vals):
        if vals.get('profile_id'):
            defaults = self._onchange_from_profile(vals)
            vals = dict(defaults, **vals)
        return super(ProductTemplate, self).create(vals)
