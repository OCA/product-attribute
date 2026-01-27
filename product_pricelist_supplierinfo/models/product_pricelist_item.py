# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2025 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("supplierinfo", "Prices based on supplier info")],
        ondelete={"supplierinfo": "set default"},
    )
    no_supplierinfo_min_quantity = fields.Boolean(
        string="Ignore Supplier Info Min. Quantity",
    )
    filter_supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier filter",
        help="Only match prices from the selected supplier",
    )
    no_supplierinfo_discount = fields.Boolean(
        string="Ignore Supplier Info Discount",
        help=(
            "If checked, the discount set on the supplier info "
            "will be ignored in price calculation."
        ),
    )
    ignore_supplierinfo_margin = fields.Boolean(
        help="Based on supplierinfo price without sale margin applied"
    )

    def get_supplier_id(self):
        self.ensure_one()
        return self.env.context.get("force_filter_supplier_id", self.filter_supplier_id)

    def _compute_base_price(self, product, quantity, uom, date, currency):
        """Compute the base price for Odoo that will be used for the full price
        computation (surcharge/discount/etc.)
        """
        price = super()._compute_base_price(product, quantity, uom, date, currency)
        rule_base = self.base or "list_price"
        if rule_base == "supplierinfo":
            context = self.env.context
            price = product.sudo()._get_supplierinfo_pricelist_price(
                self,
                quantity=quantity,
                uom=uom,
                date=date or context.get("date", fields.Date.today()),
            )
        return price
