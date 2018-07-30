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


class open_product_by_attribute_set(models.TransientModel):
    _name = 'open.product.by.attribute.set'
    _description = 'Wizard to open product by attributes set'

    attribute_set_id = fields.Many2one('attribute.set', 'Attribute Set')

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

        result = self.env.ref('product.product_template_action_all')
        result = result.read()[0]

        attribute_set = self.attribute_set_id

        grp_ids = self.env['attribute.group'].search([
            ('attribute_set_id', '=', attribute_set.id)]).ids

        result.update({
            'context': "{'open_product_by_attribute_set': %s, \
                'attribute_group_ids': %s}" % (True, grp_ids),
            'domain': "[('attribute_set_id', '=', %s)]" % attribute_set.id,
            'name': attribute_set.name,
        })

        return result
