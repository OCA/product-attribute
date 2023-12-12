# Copyright (C) 2018-Today: La Louve (<http://www.lalouve.net/>)
# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductPrintCategoryMixin(models.AbstractModel):
    _name = "product.print.category.mixin"
    _description = "Abstract Model for Product Print Categories"

    def write(self, vals):
        ProductProduct = self.env["product.product"].with_context(
            active_test=False, to_print_ok=True
        )
        ProductPrintCategory = self.env["product.print.category"]

        if "to_print" in vals or self.env.get("to_print_ok", False):
            # "to_print" is explicitely set, nothing to do
            # Or it is handled previously
            return super(
                ProductPrintCategoryMixin, self.with_context(to_print_ok=True)
            ).write(vals)

        if "print_category_id" in vals:
            # print_category_id changed, we set
            # to print, if a category is set
            # not to print if no category is set
            vals["to_print"] = bool(vals["print_category_id"])
            return super(
                ProductPrintCategoryMixin, self.with_context(to_print_ok=True)
            ).write(vals)

        # Here we have to group by print_category_id
        # and for each print_category_id we check if related fields changed
        res = super(
            ProductPrintCategoryMixin, self.with_context(to_print_ok=True)
        ).write(vals)

        if self._name == "product.template":
            domain = [
                ("product_tmpl_id", "in", self.ids),
                ("print_category_id", "!=", False),
            ]
        elif self._name == "product.product":
            domain = [
                ("print_category_id", "!=", False),
            ]
        else:
            raise NotImplementedError()
        product_groups = ProductProduct.read_group(
            domain=domain, fields=["print_category_id"], groupby="print_category_id"
        )
        products_to_update = ProductProduct
        for product_group in product_groups:

            category = ProductPrintCategory.browse(
                product_group["print_category_id"][0]
            )
            triggering_fields = category.field_ids.sudo().mapped("name")
            if len(list(set(vals.keys()) & set(triggering_fields))):
                # Value present in the label changed
                products_to_update |= ProductProduct.search(product_group["__domain"])

        if products_to_update:
            products_to_update.write({"to_print": True})
        return res
