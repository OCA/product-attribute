# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pack_line_ids = fields.One2many(
        'product.pack.line',
        'parent_product_id',
        'Pack Products',
        help='Products that are part of this pack.'
    )
    used_in_pack_line_ids = fields.One2many(
        'product.pack.line',
        'product_id',
        'Found in packs',
        help='Packs where product is used.'
    )

    @api.multi
    def get_pack_lines(self):
        """Returns the content (lines) of the packs.
        By default, return all the pack_line_ids, but that function
        can be overloaded to introduce filtering function by date, etc..."""
        return self.mapped('pack_line_ids')

    @api.multi
    def split_pack_products(self):
        """Split products and the pack in 2 separate recordsets.

        :return: [packs, no_packs]
        """
        packs = self.filtered(lambda p: p.pack_ok and p.pack_type in {
            'totalized_price',
            'none_detailed_totalized_price',
        })
        # TODO: Check why this is needed
        # for compatibility with website_sale
        if self._context.get('website_id', False) and \
                not self._context.get('from_cart', False):
            packs |= self.filtered(
                lambda p: p.pack_ok and p.pack_type == 'components_price')

        no_packs = (self | self.get_pack_lines().mapped('product_id')) - packs
        return packs, no_packs

    @api.multi
    def price_compute(self, price_type, uom=False, currency=False,
                      company=False):
        packs, no_packs = self.split_pack_products()
        prices = super(ProductProduct, no_packs).price_compute(
            price_type, uom, currency, company)
        for product in packs.with_context(prefetch_fields=False):
            pack_price = 0.0
            for pack_line in product.get_pack_lines():
                product_line_price = pack_line.product_id.price
                pack_price += (product_line_price * pack_line.quantity)
            prices[product.id] = pack_price
        return prices

    @api.depends('list_price', 'price_extra')
    def _compute_product_lst_price(self):
        packs, no_packs = self.split_pack_products()
        super(ProductProduct, no_packs)._compute_product_lst_price()
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse([self._context['uom']])
        for product in packs:
            list_price = product.price_compute('list_price').get(product.id)
            if to_uom:
                list_price = product.uom_id._compute_price(
                    list_price, to_uom)
            product.lst_price = list_price + product.price_extra
