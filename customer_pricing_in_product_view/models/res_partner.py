# -*- coding: utf-8 -*-
# © 2014 O4SB <http://o4sb.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from ast import literal_eval

from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def view_partner_pricing(self):
        """
        This function is primarily triggered by the 'Products Pricing'
        smart button on the partner form.  It returns the default product
        list action with context adjusted to set the default pricelist to
        the id of the partner.
        """
        self.ensure_one()
        act_window_model = self.env['ir.actions.act_window']
        result = act_window_model.for_xml_id(
            'product', 'product_normal_action_sell'
        )
        act_ctx = literal_eval(result['context'])
        act_ctx.update({
            'search_default_pricelist_id': self.property_product_pricelist.id
        })
        result['context'] = unicode(act_ctx)
        return result
