# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ReportProductReport_Pricelist(models.AbstractModel):
    _inherit = "report.product.report_pricelist"

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        # OVERRIDE: report one price row per packaging having its own rule in
        # the pricelist, instead of a single row in the product base UoM.
        data = super()._get_product_data(
            is_product_tmpl, product, pricelist, quantities
        )
        template = product if is_product_tmpl else product.product_tmpl_id
        has_multiple_variants = is_product_tmpl and product.product_variant_count > 1

        if template._has_multiple_uoms() and not has_multiple_variants:
            product_uoms = pricelist._get_related_uoms(product) | product.uom_id
        else:
            product_uoms = product.uom_id

        data["price"] = {
            product_uom.id: {
                qty: pricelist._get_product_price(product, qty, uom=product_uom)
                for qty in quantities
            }
            for product_uom in product_uoms
        }
        data["uoms"] = product_uoms.read(["id", "name"])

        if has_multiple_variants:
            # Flattened (variant, packaging) rows: keeps the report template a
            # single-level t-foreach instead of a nested loop, which would
            # require replacing (not just patching) the core row markup.
            data["variant_rows"] = [
                {
                    "variant_id": variant_data["id"],
                    "variant_name": variant_data["name"],
                    "uom_id": product_uom["id"],
                    "uom_name": product_uom["name"],
                    "price": variant_data["price"][product_uom["id"]],
                }
                for variant_data in data["variants"]
                for product_uom in variant_data["uoms"]
            ]

        return data
