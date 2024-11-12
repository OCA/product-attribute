# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def change_product(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.product_tmpl_id.write({})
            if rec.product_id:
                rec.product_id.write({})
        return True

    def unlink(self):
        self.change_product()
        return super(ProductPricelistItem, self).unlink()

    def write(self, vals):
        self.change_product()
        return super(ProductPricelistItem, self).write(vals)

    @api.model
    def create(self, vals):
        self.change_product()
        return super(ProductPricelistItem, self).create(vals)
