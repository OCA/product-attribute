# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
#   product_custom_attributes for OpenERP                                     #
#   Copyright (C) 2011-2013 Akretion (http://www.akretion.com/)               #
#   @author: Benoît GUILLOT <benoit.guillot@akretion.com>                     #
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


class OpenProductByAttributeSet(models.TransientModel):
    _name = 'open.product.by.attribute.set'
    _description = 'Wizard to open product by attributes set'

    attribute_set_id = fields.Many2one(
        comodel_name='attribute.set',
        string='Attribute Set')

    @api.multi
    def open_product_by_attribute(self):
        """
        Opens Product by attributes
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of account chart’s IDs
        @return: dictionary of Product list window for a given attributes set
        """
        self.ensure_one()
        attribute_set = self.attribute_set_id
        action_view = self.env.ref('product.product_normal_action', False)
        result = action_view.read()
        grp_ids = self.env['attribute.group'].search(
            [('attribute_set_id', '=', attribute_set.id)])
        ctx = "{'open_product_by_attribute_set': %s, \
              'attribute_group_ids': %s}" % (True, grp_ids)
        result['context'] = ctx
        result['domain'] = "[('attribute_set_id', '=', %s)]" % attribute_set.id
        result['name'] = attribute_set.name
        return result
