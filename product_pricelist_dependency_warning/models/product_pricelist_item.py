#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    is_base_price_changed = fields.Boolean(
        string="Base price changed",
    )

    def _has_same_product_applicability(self, item):
        """Return True iff `self` and `item` have the same applicability.

        This is not considering quantity applicability but only global/category/product/variant.
        This is not considering included categories and such, but only exact matches.
        """
        if not self and not item:
            same_applicability = True
        elif not self or not item:
            same_applicability = False
        else:
            self.ensure_one()
            item.ensure_one()
            applied_on = self.applied_on
            if applied_on != item.applied_on:
                same_applicability = False
            else:
                same_applicability = (
                    # Same global
                    applied_on == "3_global"
                    or (
                        # Same category
                        applied_on == "2_product_category"
                        and self.categ_id == item.categ_id
                    )
                    or (
                        # Same product
                        applied_on == "1_product"
                        and self.product_tmpl_id == item.product_tmpl_id
                    )
                    or (
                        # Same variant
                        applied_on == "0_product_variant"
                        and self.product_id == item.product_id
                    )
                )
        return same_applicability

    def _get_same_applicability_depending_items(self):
        """Get rules depending on the pricelist of `self` that have the same applicability."""
        # Group base price rules by their base pricelist
        base_pricelist_items = self.search(
            [
                ("base", "=", "pricelist"),
                ("base_pricelist_id", "in", self.pricelist_id.ids),
            ]
        )
        base_pricelist_to_items = {}
        for base_pricelist_item in base_pricelist_items:
            base_pricelist = base_pricelist_item.base_pricelist_id
            existing_items = base_pricelist_to_items.get(base_pricelist, self.browse())
            if not existing_items:
                base_pricelist_to_items[base_pricelist] = base_pricelist_item
            else:
                base_pricelist_to_items[base_pricelist] |= base_pricelist_item

        # Find rules having same applicability
        same_applicability_depending_items = self.browse()
        for changed_item in self:
            changed_pricelist = changed_item.pricelist_id
            depending_items = base_pricelist_to_items.get(
                changed_pricelist,
                self.browse(),
            )
            for depending_item in depending_items:
                if changed_item._has_same_product_applicability(depending_item):
                    same_applicability_depending_items |= depending_item
        return same_applicability_depending_items

    def write(self, vals):
        result = super().write(vals)
        same_applicability_depending_items = (
            self._get_same_applicability_depending_items()
        )
        same_applicability_depending_items.update(
            {
                "is_base_price_changed": True,
            }
        )
        return result
