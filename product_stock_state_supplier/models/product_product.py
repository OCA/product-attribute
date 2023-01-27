# Copyright 2023 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _selection_stock_state(self):
        res = super()._selection_stock_state()
        index = res.index(("out_of_stock", "Out Of Stock"))
        res.insert(index, (("resupplyable", "Resupplyable")))
        return res

    def _stock_state_check_resupplyable(self, qty, precision):
        return any(
            self.seller_ids.filtered(
                lambda s: (not s.product_id or s.product_id == self)
                and s.supplier_quantity > 0
            )
        )

    @api.depends(
        "seller_ids.supplier_quantity",
        "seller_ids.product_id",
    )
    def _compute_stock_state(self):
        return super()._compute_stock_state()
