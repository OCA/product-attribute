# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

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

    def get_supplier_id(self):
        self.ensure_one()
        supplier_id = self._context.get("supplier") or self.filter_supplier_id.id
        return self.env["res.partner"].browse(supplier_id)

    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        """Inherits rule computation to get price from supplierinfo"""
        if self.compute_price == "formula" and self.base == "supplierinfo":
            context = self.env.context
            price = self._compute_price_from_supplierinfo(
                price_uom=price_uom,
                product=product,
                quantity=quantity,
                partner=partner,
                date=context.get("date", fields.Date.today()),
            )
        # Re-use existing method that will apply discount/rounding/surcharge/margin
        price = super()._compute_price(price, price_uom, product, quantity, partner)
        return price

    def _compute_price_from_supplierinfo(
        self, price_uom, product, quantity, partner=False, date=False
    ):
        """Method for getting the price from supplier info.
        Please note that product could be a template or a variant
        """
        product.ensure_one()
        price = 0.0
        if self.no_supplierinfo_min_quantity:
            # No matter which minimum qty, we'll get every seller. We set a
            # number absurdidly high
            quantity = 1e9
        if type(date) == datetime:
            date = date.date()
        seller = product.with_context(
            override_min_qty=self.no_supplierinfo_min_quantity
        )._select_seller(
            # For a public user this record could be not accessible, but we
            # need to get the price anyway
            partner_id=self.sudo().get_supplier_id(),
            quantity=quantity,
            date=date,
        )
        if seller:
            # Get seller price in product's purchase UoM
            price = seller._get_supplierinfo_pricelist_price()
            # Convert the price if wanted in another UoM
            if price_uom.id != seller.product_uom.id:
                price = seller.product_uom._compute_price(price, price_uom)
            if price:
                # Also convert the price if the pricelist and seller have
                # different currencies so the price have the pricelist currency
                if self.currency_id != seller.currency_id:
                    convert_date = date or self.env.context.get(
                        "date", fields.Date.today()
                    )
                    price = seller.currency_id._convert(
                        price, self.currency_id, seller.company_id, convert_date
                    )
        return price
