# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    price_ids = fields.One2many(
        comodel_name='product.multi.price',
        compute='_compute_price_ids',
        inverse='_inverse_price_ids',
        string="Other Prices",
    )

    @api.depends('product_variant_ids',
                 'product_variant_ids.price_ids')
    def _compute_price_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.price_ids = p.product_variant_ids.price_ids

    def _inverse_price_ids(self):
        for p in self:
            if len(p.product_variant_ids) == 1:
                p.product_variant_ids.price_ids = p.price_ids

    def _get_multiprice_pricelist_price(self, rule):
        if len(self.product_variant_ids) == 1:
            return (
                self.product_variant_ids._get_multiprice_pricelist_price(rule))
        return 0

    @api.model
    def create(self, vals):
        """Overwrite creation for rewriting the prices (if set and having only
        one variant), after the variant creation, that is performed in super.
        """
        template = super().create(vals)
        if vals.get('price_ids'):
            template.write({
                'price_ids': vals.get('price_ids'),
            })
        return template

    def price_compute(self, price_type, uom=False, currency=False,
                      company=False):
        """Return temporary prices when computation is done for multi price for
        avoiding error on super method. We will later fill these with the
        correct values.
        """
        if price_type == 'multi_price':
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
