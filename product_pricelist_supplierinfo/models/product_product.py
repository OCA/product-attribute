# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_supplierinfo_pricelist_price(
            self, rule, date=None, quantity=None):
        return self.product_tmpl_id._get_supplierinfo_pricelist_price(
            rule, date=date, quantity=quantity, product_id=self.id)

    def price_compute(self, price_type, uom=False, currency=False,
                      company=False):
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == 'supplierinfo':
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company)
