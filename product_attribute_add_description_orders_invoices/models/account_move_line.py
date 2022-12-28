# Copyright 2022 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_name(self):
        self.ensure_one()
        res = super()._get_computed_name()
        name = "{}{}".format(res, "\n")
        attribute_values = (
            self.product_id.product_template_attribute_value_ids.attribute_line_id
        )
        variants = self.env["product.template.attribute.line"].search(
            [("product_tmpl_id", "=", self.product_id.product_tmpl_id.id)]
        )
        product_attibute_lines = (
            self.product_id.product_template_attribute_value_ids.product_attribute_value_id
        )
        for variant in variants:
            if variant.attribute_id.show_in_sale_invoices:
                attribute_values |= variant
        for attribute_value in attribute_values:
            if attribute_value.attribute_id.show_in_sale_invoices:
                values_to_add = [
                    value.display_name
                    for value in attribute_value.value_ids
                    if value.id in product_attibute_lines.ids
                ]
                if (
                    attribute_value.attribute_id.create_variant == "no_variant"
                    and not values_to_add
                ):
                    values_to_add.append(attribute_value.value_ids[0].display_name)
                name += "{}{}".format("\n", "\n".join(values_to_add))
        return name
