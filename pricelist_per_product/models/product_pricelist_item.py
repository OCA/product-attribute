# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    related_sequence = fields.Integer(
        string='Sequence',
        related='sequence',
        help="Allows modification of the sequence manually as "
             "the sequence field is difficult to modify due to 'handle'."
    )

    @api.model
    def _get_sequence_price_grid(self, vals):
        """ This method returns a lower sequence number for the
        ``product.pricelist.item`` associated with the product variants
        and a higher sequence number for the ``product.pricelist.item``
        associated with product templates. This allows us
        to use the ``product.pricelist.item`` for a variant over the
        one for the template in  ``sale.order.lines`` """
        product_id = vals.get('product_id', self.product_id)
        product_tmpl_id = vals.get('product_tmpl_id', self.product_tmpl_id)
        related_sequence = 15
        if product_id:
            related_sequence = 5
        elif product_tmpl_id:
            related_sequence = 10
        return related_sequence

    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            vals['related_sequence'] = self._get_sequence_price_grid(vals)
        return super(ProductPricelistItem, self).create(vals)

    @api.multi
    def write(self, vals):
        for item in self:
            if vals.get('product_id'):
                vals['related_sequence'] = item._get_sequence_price_grid(vals)
            super(ProductPricelistItem, item).write(vals)
        return True
