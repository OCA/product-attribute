
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) All Rights Reserved 2015 Akretion
#    @author Abdessamad HILALI <abdessamad.hilali@akretion.com>
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
###############################################################################
from openerp import models, api
from lxml import etree
from openerp.osv import orm


class ProductVariants(models.Model):
    _inherit = 'product.product'

    @api.multi
    def button_activate(self):
        self.active = True

    @api.multi
    def button_deactivate(self):
        self.active = False

    @api.model
    def fields_view_get(self,
                        view_id=None,
                        view_type='tree',
                        toolbar=False, submenu=False):
        """ Dynamic modification of fields """
        res = super(ProductVariants, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu)
        root = etree.fromstring(res['arch'])
        if view_type == 'tree':
            for button in root.findall(".//button"):
                if 'search_disable_custom_filters' in self.env.context:
                    button.set('invisible', '0')
                    orm.setup_modifiers(button, root)
            res['arch'] = etree.tostring(root, pretty_print=True)
        return res
