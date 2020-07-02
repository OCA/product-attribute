# Copyright 2017-Today GRAP (http://www.grap.coop).
# Copyright 2018 ACSONE SA/NV
# Copyright 2018 Akretion (http://www.akretion.com).
# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Laurent Mignon <laurent.mignon@acsone.com>
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    _STOCK_STATE_SELECTION = [
        ("in_stock", "In Stock"),
        ("in_limited_stock", "In Limited Stock"),
        ("resupplying", "Resupplying"),
        ("out_of_stock", "Out Of Stock"),
    ]

    stock_state = fields.Selection(
        selection="_selection_stock_state", compute="_compute_stock_state"
    )

    def _selection_stock_state(self):
        return self._STOCK_STATE_SELECTION

    def _get_qty_available_for_stock_state(self):
        """
        This method can be overridden to provide the available qty.
        In some cases you could prefer to use the qty_available - outgoing_qty
        to take into account products reserved
        """
        self.ensure_one()
        return self.qty_available

    def _stock_state_check_in_stock(self, qty, precision):
        return (
            float_compare(
                qty, self._get_stock_state_threshold(), precision_digits=precision,
            )
            == 1
        )

    def _stock_state_check_in_limited_stock(self, qty, precision):
        return float_compare(qty, 0, precision_digits=precision) == 1

    def _stock_state_check_resupplying(self, qty, precision):
        return float_compare(self.incoming_qty, 0, precision_digits=precision) == 1

    def _stock_state_check_out_of_stock(self, qty, precision):
        return True

    def _available_states(self):
        return [x[0] for x in self._selection_stock_state()]

    @api.depends(
        "qty_available",
        "incoming_qty",
        "stock_state_threshold",
        "company_id.stock_state_threshold",
    )
    def _compute_stock_state(self):
        for product in self:
            qty_available = product._get_qty_available_for_stock_state()
            precision = self.env["decimal.precision"].precision_get("Stock Threshold")
            stock_state = False
            for state in self._available_states():
                checker = getattr(product, "_stock_state_check_" + state)
                if checker(qty_available, precision):
                    stock_state = state
                    break
            product.stock_state = stock_state

    def _get_stock_state_threshold(self):
        self.ensure_one()
        threshold = self.stock_state_threshold
        if not threshold:
            # try to get threshold from current company
            threshold = self.env.company.stock_state_threshold
        return threshold
