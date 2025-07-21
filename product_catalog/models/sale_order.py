# Copyright 2025 Kencove (http://www.kencove.com).
# @author Mohamed Alkobrosli <malkobrosly@kencove.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def custom_add_from_catalog(self):
        kanban_view_id = self.env.ref("product_catalog.product_view_kanban_catalog").id
        search_view_id = self.env.ref("product_catalog.product_view_search_catalog").id
        additional_context = self._get_action_add_from_catalog_extra_context()
        return {
            "type": "ir.actions.act_window",
            "name": _("Products"),
            "res_model": "product.product",
            "views": [(kanban_view_id, "kanban"), (False, "form")],
            "search_view_id": [search_view_id, "search"],
            "domain": self._get_product_catalog_domain(),
            "context": {**self.env.context, **additional_context},
        }

    def _get_product_catalog_domain(self):
        return [
            "|",
            ("company_id", "=", False),
            ("company_id", "parent_of", self.company_id.id),
            ("type", "!=", "combo"),
        ]

    def _get_action_add_from_catalog_extra_context(self):
        return {
            "product_catalog_order_id": self.id,
            "product_catalog_order_model": self._name,
            "product_catalog_currency_id": self.currency_id.id,
            "product_catalog_digits": self.order_line._fields["price_unit"].get_digits(
                self.env
            ),
        }
