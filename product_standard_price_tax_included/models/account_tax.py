# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math
from odoo import api, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.multi
    def _compute_amount(
            self, base_amount, price_unit, quantity=1.0, product=None,
            partner=None):
        """Patch this function, if use_force_price_include is True
        the compute_all function allow to override vat price_include,
        using in the context the key force_price_include
        but in the _compute_amount function, it is not possible.
        so we override this function in this case.
        """
        if not self.env.context.get('use_force_price_include', False):
            return super()._compute_amount(
                base_amount, price_unit, quantity=quantity, product=product,
                partner=partner)

        self.ensure_one()
        if self.amount_type == 'fixed':
            if base_amount:
                return math.copysign(quantity, base_amount) * self.amount
            else:
                return quantity * self.amount

        # Note This is the unique line altered, comparing to the original
        # function
        price_include =\
            self._context.get('force_price_include', self.price_include)

        if (self.amount_type == 'percent' and not price_include)\
                or (self.amount_type == 'division' and price_include):
            return base_amount * self.amount / 100
        if self.amount_type == 'percent' and price_include:
            return base_amount - (base_amount / (1 + self.amount / 100))
        if self.amount_type == 'division' and not price_include:
            return base_amount / (1 - self.amount / 100) - base_amount
