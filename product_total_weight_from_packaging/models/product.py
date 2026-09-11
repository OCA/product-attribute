# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_total_weight_from_packaging(self, qty):
        """Estimate the weight of `qty` using the weight of its packagings.

        Packagings without a weight are ignored, hence the quantity they would
        have covered is spread over the smaller packagings and, in the end,
        over the product's own weight.
        """
        self.ensure_one()
        weight_by_uom = self._packaging_weight_by_uom()
        qty_by_packaging_with_weight = self.with_context(
            _packaging_filter=lambda uom: uom.id in weight_by_uom,
            _packaging_values_handler=lambda packaging, qty_per_pkg: (
                self._prepare_qty_by_packaging_values_with_weight(
                    packaging, qty_per_pkg, weight_by_uom
                )
            ),
        ).product_qty_by_packaging(qty)
        return sum(
            values["qty"] * values["weight"] for values in qty_by_packaging_with_weight
        )

    def _packaging_weight_by_uom(self):
        """Return the weight of the packagings having one, by packaging UoM id."""
        self.ensure_one()
        return {
            packaging.uom_id.id: packaging.weight
            for packaging in self.packaging_ids
            if packaging.weight
        }

    def _prepare_qty_by_packaging_values_with_weight(
        self, packaging_tuple, qty_per_pkg, weight_by_uom
    ):
        # Packaging weights and the product weight are both expressed in the
        # product's weight UoM, no conversion is needed.
        weight = (
            self.weight
            if packaging_tuple.is_unit
            else weight_by_uom.get(packaging_tuple.id, 0.0)
        )
        return {"qty": qty_per_pkg, "weight": weight}
