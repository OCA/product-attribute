# Copyright 2019- WT-IO-IT GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    rule_price = fields.Float(
        string='Rule UoM Price',
        digits=dp.get_precision('Product Price'), default=0.0,
        help='The price to purchase a product',
    )

    product_uom_category_id = fields.Many2one(
        comodel_name='uom.category',
        string='Product UoM Category',
        related='product_uom.category_id',
    )

    rule_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Rule for UoM',
        domain="[('category_id', '=', product_uom_category_id)]",
    )

    @api.onchange('rule_price', 'rule_uom_id')
    def onchange_rule_qty_uom(self):
        if not self.rule_uom_id and self.rule_price:
            self.rule_price = False
        if self.rule_uom_id and not self.rule_price:
            self.rule_price = self.rule_uom_id._compute_quantity(
                self.price, self.product_uom
            )

        if not (self.rule_uom_id and self.rule_price):
            return
        self.price = self.product_uom._compute_quantity(
            self.rule_price, self.rule_uom_id
        )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _select_seller(
        self, partner_id=False, quantity=0.0,
        date=None, uom_id=False, params=False
    ):
        sellers = super(ProductProduct, self)._select_seller(
            partner_id=partner_id, quantity=quantity,
            date=date, uom_id=uom_id, params=params
        )

        matching_rule_uom = self.env['product.supplierinfo']
        for seller in sellers:
            if (
                uom_id != seller.product_uom and
                seller.rule_uom_id and
                seller.rule_uom_id == uom_id
            ):
                matching_rule_uom |= seller

        if not matching_rule_uom:
            return sellers
        return matching_rule_uom
