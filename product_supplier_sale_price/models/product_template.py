# Copyright 2021 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'list_price' in vals:
            if vals['list_price']:
                use_supplier_sale_price = False
            elif not vals['list_price']:
                use_supplier_sale_price = True
            for product in self.product_variant_ids:
                product.use_supplier_sale_price = use_supplier_sale_price

        return res

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if 'list_price' in vals:
            if vals['list_price']:
                use_supplier_sale_price = False
            elif not vals['list_price']:
                use_supplier_sale_price = True
            for product in res.product_variant_ids:
                product.use_supplier_sale_price = use_supplier_sale_price

        return res
