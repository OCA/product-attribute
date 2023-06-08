# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """Adding date to context in order to retrieve it from the rule as this value
        is not passed as a variable in `_compute_price`
        """
        if date and "date" not in self._context:
            self = self.with_context(date=date)
        return super(ProductPricelist, self)._compute_price_rule(
            products_qty_partner, date, uom_id
        )
