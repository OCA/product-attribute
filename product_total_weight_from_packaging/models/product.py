# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class ProductProduct(models.Model):

    _inherit = "product.product"

    def get_total_weight_from_packaging(self, qty):
        self.ensure_one()
        qty_by_packaging_with_weight = self.with_context(
            **{
                "_packaging_filter": lambda p: p.max_weight,
                "_packaging_values_handler": self._prepare_qty_by_packaging_values_with_weight,  # noqa
            }
        ).product_qty_by_packaging(qty)
        total_weight = sum(
            [
                pck.get("qty", 0) * pck.get("weight", 0)
                for pck in qty_by_packaging_with_weight
            ]
        )
        return total_weight

    def _prepare_qty_by_packaging_values_with_weight(
        self, packaging_tuple, qty_per_pkg
    ):
        res = {
            "qty": qty_per_pkg,
        }
        if packaging_tuple.is_unit:
            res["weight"] = self.weight
        else:
            packaging = self.env["product.packaging"].browse(packaging_tuple.id)
            res["weight"] = packaging.max_weight
        return res
