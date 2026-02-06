from __future__ import annotations

from typing import TYPE_CHECKING

from odoo import models, tools

if TYPE_CHECKING:
    from odoo.tools.float_utils import RoundingMethod


class UomUom(models.Model):
    _inherit = "uom.uom"

    def _get_product_uom_factor(self, product_id, from_uom, to_uom):
        """Look up the product-specific cross-category conversion factor.

        Returns the factor to multiply the quantity by when converting from
        from_uom to to_uom for the given product, or None if no
        product-specific factor applies.

        Strategy: convert from_uom → product base UoM → to_uom.
        For each leg, if the UoM is in the same category as the base UoM,
        use the standard UoM factor. If cross-category, find the
        product.uom.factor record whose uom_id shares a category with
        that UoM, and use its
        factor combined with the standard intra-category conversion.
        """
        product = self.env["product.product"].browse(product_id)
        if not product.exists():
            return None
        base_uom = product.uom_id

        from_is_cross = not base_uom._has_common_reference(from_uom)
        to_is_cross = not base_uom._has_common_reference(to_uom)

        # Leg 1: from_uom → base_uom (in base_uom units)
        if from_is_cross:
            puom = self._find_product_uom_for_category(product_id, from_uom)
            # qty_base = qty * (from_uom.factor / puom.uom_id.factor) * puom.factor
            # i.e. convert from_uom to the packaging reference, then apply factor
            from_to_base = from_uom.factor / puom.uom_id.factor * puom.factor
        else:
            # Standard intra-category: from_uom → base_uom
            from_to_base = from_uom.factor / base_uom.factor

        # Leg 2: base_uom → to_uom (multiplier to get to_uom units)
        if to_is_cross:
            puom = self._find_product_uom_for_category(product_id, to_uom)
            # base_to_to = (puom.uom_id.factor / to_uom.factor) / puom.factor
            base_to_to = puom.uom_id.factor / to_uom.factor / puom.factor
        else:
            # Standard intra-category: base_uom → to_uom
            base_to_to = base_uom.factor / to_uom.factor

        return from_to_base * base_to_to

    def _find_product_uom_for_category(self, product_id, uom):
        """Find the product.uom.factor record whose uom_id is in the same
        category as the given uom.

        Searches for factors that apply to the given product variant:
        either variant-specific (product_ids contains the variant) or
        template-wide (product_ids is empty). Variant-specific factors
        take precedence.
        """
        if not isinstance(product_id, int):
            return None
        product = self.env["product.product"].browse(product_id)
        Factor = self.env["product.uom.factor"]
        domain = [
            ("product_tmpl_id", "=", product.product_tmpl_id.id),
            "|",
            ("product_ids", "=", False),
            ("product_ids", "in", product_id),
        ]
        # First try exact UoM match
        exact = Factor.search(
            domain + [("uom_id", "=", uom.id)],
            limit=1,
        )
        if exact:
            return exact
        # Find any factor in the same category
        for f in Factor.search(domain):
            if f.uom_id._has_common_reference(uom):
                return f

    def _compute_quantity(
        self,
        qty,
        to_unit,
        round=True,
        rounding_method: RoundingMethod = "UP",
        raise_if_failure=True,
    ):
        if self != to_unit:
            self.ensure_one()
            product_id = self.env.context.get("product_id")
            if product_id and not self._has_common_reference(to_unit):
                conversion = self._get_product_uom_factor(product_id, self, to_unit)
                if conversion is not None:
                    amount = qty * conversion
                    if to_unit and round:
                        amount = tools.float_round(
                            amount,
                            precision_rounding=to_unit.rounding,
                            rounding_method=rounding_method,
                        )
                    return amount
        return super()._compute_quantity(
            qty,
            to_unit,
            round=round,
            rounding_method=rounding_method,
            raise_if_failure=raise_if_failure,
        )

    def _compute_price(self, price, to_unit):
        if self != to_unit:
            self.ensure_one()
            product_id = self.env.context.get("product_id")
            if product_id and not self._has_common_reference(to_unit):
                conversion = self._get_product_uom_factor(product_id, self, to_unit)
                if conversion is not None:
                    return price / conversion
        return super()._compute_price(price, to_unit)
