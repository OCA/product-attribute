# Copyright 2017-Today GRAP (http://www.grap.coop).
# Copyright 2018 ACSONE SA/NV
# Copyright 2018 Akretion (http://www.akretion.com).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Laurent Mignon <laurent.mignon@acsone.com>
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
        selection=_STOCK_STATE_SELECTION, compute="_compute_stock_state"
    )

    def _get_qty_available_for_stock_state(self):
        """
        This method can be overridden to provide the available qty.
        In some cases you could prefer to use the qty_available - outgoing_qty
        to take into account products reserved
        """
        self.ensure_one()
        return self.qty_available

    @api.depends("qty_available", "incoming_qty")
    def _compute_stock_state(self):
        for product in self:
            qty_available = product._get_qty_available_for_stock_state()
            precision = self.env["decimal.precision"].precision_get("Stock Threshold")
            if (
                float_compare(
                    qty_available,
                    product._get_stock_state_threshold(),
                    precision_digits=precision,
                )
                == 1
            ):
                product.stock_state = "in_stock"
            elif float_compare(qty_available, 0, precision_digits=precision,) == 1:
                product.stock_state = "in_limited_stock"
            elif (
                float_compare(product.incoming_qty, 0, precision_digits=precision,) == 1
            ):
                product.stock_state = "resupplying"
            else:
                product.stock_state = "out_of_stock"

    def _get_stock_state_threshold(self):
        self.ensure_one()
        threshold = self.stock_state_threshold
        if not threshold:
            # try to get threshold from current company
            threshold = self.env.user.company_id.stock_state_threshold
        return threshold
