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

    def _compute_price(self, product, quantity, uom, date, currency=None, **kwargs):
        result = super()._compute_price(
            product, quantity, uom, date, currency, **kwargs
        )
        context = self.env.context
        if self.compute_price == "formula" and self.base == "supplierinfo":
            result = product.sudo()._get_supplierinfo_pricelist_price(
                self,
                date=date or context.get("date", fields.Date.today()),
                quantity=quantity,
            )
            # When ignoring the supplier discount, the raw seller price is used
            # which is expressed in the seller's purchase UoM. Convert it to the
            # product's sale UoM so that _compute_price_rule receives a
            # consistent price regardless of the seller's UoM.
            if result and self.no_supplierinfo_discount:
                seller = (
                    product.sudo()
                    .with_context(override_min_qty=self.no_supplierinfo_min_quantity)
                    ._select_seller(
                        partner_id=context.get(
                            "force_filter_supplier_id", self.sudo().filter_supplier_id
                        ),
                        quantity=quantity,
                        date=date or context.get("date", fields.Date.today()),
                    )
                )
                if seller and seller.product_uom_id != product.uom_id:
                    result = seller.product_uom_id._compute_price(
                        result, product.uom_id
                    )
        return result
