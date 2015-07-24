# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com).
#        Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def _price_field_get_ext(self):
        """Add fixed price to pricetype selection."""
        result = super(ProductPricelistItem, self)._price_field_get()
        result.append((-3, _('Fixed Price')))
        return result

    @api.onchange('base_ext')
    def change_base_ext(self):
        if self.base_ext == -3:
            base = self.env['product.price.type'].search(
                [], limit=1, order='id'
            )
            self.base = base[0]
            self.price_discount = -1

    base_ext = fields.Selection(
        selection='_price_field_get_ext',
        string='Based on',
        required=True,
        size=-1,
        default=-1,
        help="Base price for computation",
    )
