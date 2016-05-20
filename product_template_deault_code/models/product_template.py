
# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, api, fields, _

class ProductTemplate(models.Model):
    """
    Name get product template
    """
    _inherit = "product.template"
    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name','')
            code = self.env.context.get('display_default_code', True) and d.get('default_code',False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)
        result = []
        for product in self:
            mydict = {
                'id': product.id,
                'name': product.name,
                'default_code':product.default_code,
            }
            result.append(_name_get(mydict))
        return result
