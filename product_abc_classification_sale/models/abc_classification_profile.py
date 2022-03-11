# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ABCClassificationProfile(models.Model):
    _inherit = "abc.classification.profile"

    data_source = fields.Selection(selection_add=([("sale_report", "Sales Report")]))
    value_criteria = fields.Selection(
        selection_add=([("sold_delivered_value", "Sold Delivered Value")])
    )

    def _fill_initial_product_data(self, date, date_end=False):
        if self.data_source == "sale_report":
            return self._fill_data_from_sale_report(date, [], date_end=date_end)
        return super()._fill_initial_product_data(date, date_end=date_end)

    def _fill_data_from_sale_report(self, date, product_list, date_end=False):
        domain = [
            ("state", "in", ["sale", "done"]),
            ("date", ">=", date),
            ("qty_delivered", ">", 0),
            "|",
            ("product_id.abc_classification_profile_id", "=", self.id),
            "|",
            ("product_id.categ_id.abc_classification_profile_id", "=", self.id),
            (
                "product_id.categ_id.parent_id.abc_classification_profile_id",
                "=",
                self.id,
            ),
        ]
        if date_end:
            domain.append(("date", "<=", date_end))
        sales_report = self.env["sale.report"].read_group(
            domain,
            ["product_id", "price_subtotal", "product_uom_qty", "qty_delivered"],
            ["product_id"],
        )
        for result in sales_report:
            product_uom_qty = result["product_uom_qty"]
            product_data = {
                "product": self.env["product.product"].browse(result["product_id"][0]),
                "units_sold": product_uom_qty,
                "price_subtotal_delivered": product_uom_qty
                and (result.get("price_subtotal") / result.get("product_uom_qty"))
                * result.get("qty_delivered")
                or 0,
            }
            product_list.append(product_data)
        return product_list

    def _fill_data_from_stock_moves(self, date, product_list, date_end=False):
        product_list = super()._fill_data_from_stock_moves(
            date, product_list, date_end=False
        )
        for product_data in product_list:
            product_data["price_subtotal_delivered"] = (
                product_data["product"].list_price * product_data["units_sold"]
            )
        return product_list

    def _get_inventory_product_value(self, data):
        self.ensure_one()
        if self.value_criteria == "sold_delivered_value":
            return data["price_subtotal_delivered"]
        return super()._get_inventory_product_value(data)
