from odoo import models

from ..constants import constants as core_constants


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _compute_price_rule_get_items(
        self, products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids
    ):
        res = super(ProductPricelist, self)._compute_price_rule_get_items(
            products_qty_partner=products_qty_partner,
            date=date,
            uom_id=uom_id,
            prod_tmpl_ids=prod_tmpl_ids,
            prod_ids=prod_ids,
            categ_ids=categ_ids,
        )
        dim_vals = {}
        for context_key in self.env.context:
            if context_key in core_constants.LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT:
                dim_vals[context_key] = self.env.context.get(context_key, 0)
        dim_vals = core_constants.check_dim_vals(dim_vals)
        items = self.env["product.pricelist.item"]
        have_dimensions = False
        if dim_vals and sum([item[1] for item in dim_vals.items()]) > 0:
            have_dimensions = True
        for price_list_item in res:
            if not price_list_item.use_dim_rules:
                items = items | price_list_item
                continue
            dimensions_mathes_pricelist_list = []
            for product_dimension in dim_vals:
                try:
                    dimension = product_dimension.split("_")[1]
                    dimension_value = dim_vals[product_dimension]
                    dimension_from = getattr(price_list_item, dimension + "_from")
                    dimension_to = getattr(price_list_item, dimension + "_to")
                    if dimension_from == 0.0 and dimension_to == 0.0:
                        dimensions_mathes_pricelist_list.append(None)
                        continue
                    is_match = core_constants.match_value(
                        dimension_value, dimension_from, dimension_to
                    )
                    dimensions_mathes_pricelist_list.append(is_match)
                except AttributeError:
                    dimensions_mathes_pricelist_list.append(None)
            dimensions_mathes_pricelist_list = list(
                filter(lambda item: item is not None, dimensions_mathes_pricelist_list)
            )
            if all(dimensions_mathes_pricelist_list) and have_dimensions:
                items = items | price_list_item
        return items
