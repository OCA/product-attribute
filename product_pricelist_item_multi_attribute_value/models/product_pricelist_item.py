# Copyright 2025 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    have_additional_price = fields.Boolean(
        compute="_compute_have_additional_price",
        help="Check if the product has an additional price",
        search="_search_have_additional_price",
    )

    pricelist_item_attribute_value_ids = fields.One2many(
        comodel_name="product.pricelist.item.attribute.value",
        inverse_name="pricelist_item_id",
        string="Attribute Values",
    )

    @api.depends("pricelist_item_attribute_value_ids")
    def _compute_have_additional_price(self):
        for item in self:
            item.have_additional_price = any(item.pricelist_item_attribute_value_ids)

    def get_additional_price_from_attributes(self, product):
        if product._name == "product.product":
            product_value_ids = set(
                product.product_template_variant_value_ids.mapped(
                    "product_attribute_value_id"
                ).ids
            )
            return sum(
                item.additional_price
                for item in self.pricelist_item_attribute_value_ids
                if product_value_ids.intersection(item.attribute_value_ids.ids)
            )
        return 0.0

    def _compute_price(self, product, quantity, uom, date, currency=None):
        price = super()._compute_price(product, quantity, uom, date, currency=currency)
        if self.have_additional_price and self.applied_on == "1_product":
            price += self.get_additional_price_from_attributes(product)
        return price

    def _search_have_additional_price(self, operator, value):
        if operator in ["=", "!="]:
            return [("pricelist_item_attribute_value_ids", operator, True)]

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        copied_values = []
        for line in self.pricelist_item_attribute_value_ids:
            line_vals = line.copy_data()[0]
            line_vals["pricelist_item_id"] = False
            copied_values.append((0, 0, line_vals))
        default["pricelist_item_attribute_value_ids"] = copied_values
        return super().copy(default=default)
