# Copyright 2022 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_sale_order_line_multiline_description_variants(self):
        super()._get_sale_order_line_multiline_description_variants()
        name = "\n"
        custom_attribute_ids = self.product_custom_attribute_value_ids
        custom_ptavs = custom_attribute_ids.custom_product_template_attribute_value_id
        attribute_values = self.product_id.product_template_attribute_value_ids
        no_variant_ptavs = self.product_no_variant_attribute_value_ids._origin
        for ptav in set((no_variant_ptavs - custom_ptavs) + attribute_values):
            if ptav.attribute_id.show_in_sale_invoices:
                name += "\n" + ptav.display_name
        custom_values = sorted(
            self.product_custom_attribute_value_ids,
            key=lambda r: (r.custom_product_template_attribute_value_id.id, r.id),
        )
        for pacv in custom_values:
            attribute = pacv.custom_product_template_attribute_value_id.attribute_id
            if attribute.show_in_sale_invoices:
                name += "\n" + pacv.display_name
        return name
