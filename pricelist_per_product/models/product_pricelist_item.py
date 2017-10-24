# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.model
    def _check_applied_on_coherence(self, vals):
        """ This method checks if applied_on field has the correct value.
        This allows us to use the ``product.pricelist.item``
        for a variant over the one for the template in
        ``sale.order.line`` or ``purchase.order.line``.
        This module is useful when we import pricelist.item or
        create it by web service.
        """
        if vals.get('product_tmpl_id') and\
                vals.get('applied_on') != '1_product':
            vals['applied_on'] = '1_product'
        if vals.get('product_id') and\
                vals.get('applied_on') != '0_product_variant':
            vals['applied_on'] = '0_product_variant'
        return vals

    @api.model
    def create(self, vals):
        vals = self._check_applied_on_coherence(vals)
        return super(ProductPricelistItem, self).create(vals)

    @api.multi
    def write(self, vals):
        vals = self._check_applied_on_coherence(vals)
        return super(ProductPricelistItem, self).write(vals)
