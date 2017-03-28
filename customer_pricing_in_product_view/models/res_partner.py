# -*- coding: utf-8 -*-
# Copyright 2014 Odoo Community Association (OCA), O4SB - Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def open_product_pricing(self):  # pragma: no cover
        """
        Opens the product form with defaults set to view customer pricing.
        Setting pricelist: True unhides the price column. Excluded from
        testing as does nothing except update a context.
        :return: a view dictionary
        """
        self.ensure_one()
        action = self.env.ref('product.product_normal_action')
        result = action.read()[0]
        result['context'] = {
            'pricelist': True,
            'search_default_pricelist_id': self.property_product_pricelist.id
        }
        return result
