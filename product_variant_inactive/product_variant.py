# coding: utf-8
# © 2015 Abdessamad HILALI <abdessamad.hilali@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from lxml import etree
from openerp.osv import orm


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def button_activate(self):
        self.write({'active': True})

    @api.multi
    def button_deactivate(self):
        self.write({'active': False})

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree',
                        toolbar=False, submenu=False):
        """ Dynamic modification of fields """
        res = super(ProductProduct, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        root = etree.fromstring(res['arch'])
        if view_type == 'tree':
            for button in root.findall(".//button"):
                # search_disable_custom_filters is applied when active_id/ids
                # defined in addons/web/static/src/js/views.js
                if 'search_disable_custom_filters' in self.env.context:
                    button.set('invisible', '0')
                    orm.setup_modifiers(button, root)
            res['arch'] = etree.tostring(root, pretty_print=True)
        return res
