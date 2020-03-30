# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    price_ids = fields.One2many(
        comodel_name='product.multi.price',
        compute='_compute_price_ids',
        inverse='_set_price_ids',
    )
    multi_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        compute='_compute_multi_price',
        groups="base.group_user",
        readonly=True,
    )

    @api.depends('product_variant_ids',
                 'product_variant_ids.price_ids')
    def _compute_price_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.price_ids = p.product_variant_ids.price_ids

    def _set_price_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.product_variant_ids.price_ids = p.price_ids

    def _get_multiprice_pricelist_price(self, rule):
        if len(self.product_variant_ids) == 1:
            return (
                self.product_variant_ids._get_multiprice_pricelist_price(rule))
        return 0

    @api.depends('product_variant_ids', 'product_variant_ids.multi_price')
    def _compute_multi_price(self):
        """Use multi_price field as the frontend for any of the registered
           multi price fields on the product passing it by context"""
        multi_price_field = self.env.context.get('multi_price_field', False)
        if not multi_price_field:
            self.update({'multi_price': 0})
            return
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.multi_price = p.product_variant_ids.multi_price

    @api.model
    def create(self, vals):
        product = super().create(vals)
        if vals.get('price_ids'):
            product.write({
                'price_ids': vals.get('price_ids'),
            })
        return product
