# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2025 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools import format_amount


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

    def _compute_price(self, product, quantity, uom, date, currency=None):
        # We need to pass the rule and quantity to the product to be able to
        # get the right price from _get_supplierinfo_pricelist_price.
        product = product.with_context(
            supplierinfo_rule=self.id, supplierinfo_quantity=quantity
        )
        result = super()._compute_price(product, quantity, uom, date, currency)
        return result

    def _compute_price_label(self):
        pricelist_items_to_update = self.filtered(
            lambda r: r.compute_price != "fixed" and r.base == "supplierinfo"
        )
        for item in pricelist_items_to_update:
            base_str = self.env._("supplier's price")
            # Replicate standard label computation with new base string
            extra_fee_str = ""
            if item.price_surcharge > 0:
                extra_fee_str = self.env._(
                    "+ %(amount)s extra fee",
                    amount=format_amount(
                        item.env,
                        abs(item.price_surcharge),
                        currency=item.currency_id,
                    ),
                )
            elif item.price_surcharge < 0:
                extra_fee_str = self.env._(
                    "- %(amount)s rebate",
                    amount=format_amount(
                        item.env,
                        abs(item.price_surcharge),
                        currency=item.currency_id,
                    ),
                )
            discount_type, percentage = self._get_displayed_discount(item)
            item.price = self.env._(
                "%(percentage)s %% %(discount_type)s on %(base)s %(extra)s",
                percentage=percentage,
                discount_type=discount_type,
                base=base_str,
                extra=extra_fee_str,
            )
        return super(
            ProductPricelistItem, self - pricelist_items_to_update
        )._compute_price_label()
