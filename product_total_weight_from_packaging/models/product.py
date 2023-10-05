# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class ProductProduct(models.Model):

    _inherit = "product.product"

    def get_total_weight_from_packaging(self, qty):
        self.ensure_one()
        qty_by_packaging_with_weight = self.with_context(
            **{
                "_packaging_filter": lambda p: p.weight,
                "_packaging_values_handler": self._prepare_qty_by_packaging_values_with_weight,  # noqa
            }
        ).product_qty_by_packaging(qty)
        # Convert to the uom of the product
        total_weight = 0

        for packaging in qty_by_packaging_with_weight:
            weight_uom_id = packaging.get("weight_uom_id")
            quantity = packaging.get("qty", 0)
            weight = packaging.get("weight", 0)

            uom = self.env["uom.uom"].browse(weight_uom_id)
            weight_in_product_uom = uom._compute_quantity(
                qty=quantity * weight,
                to_unit=self.product_tmpl_id.weight_uom_id,
                round=False,
            )
            total_weight += weight_in_product_uom
        return total_weight

    def _prepare_qty_by_packaging_values_with_weight(
        self, packaging_tuple, qty_per_pkg
    ):
        res = {
            "qty": qty_per_pkg,
        }
        if packaging_tuple.is_unit:
            res["weight"] = self.product_weight
            res["weight_uom_id"] = self.product_tmpl_id.weight_uom_id.id
        else:
            packaging = self.env["product.packaging"].browse(packaging_tuple.id)
            res["weight"] = packaging.weight
            res["weight_uom_id"] = packaging.weight_uom_id.id
        return res
