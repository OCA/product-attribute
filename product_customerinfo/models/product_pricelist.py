# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.multi
    def price_rule_get(self, prod_id, qty, partner=None):
        """Pass context if the type of the pricelist is sale for restricting
        on the search product.supplierinfo records of type customer."""
        obj = (self.with_context(supplierinfo_type='customer') if
               self.type == 'sale' else self)
        return super(ProductPricelist, obj).price_rule_get(
            prod_id, qty, partner=partner)
