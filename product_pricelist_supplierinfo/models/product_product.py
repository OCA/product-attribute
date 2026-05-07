# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_sellers(self, params=False):
        """When we override min qty we want that _select_sellers gives us the
        first possible seller for every other criteria ignoring the quantity. As
        supplierinfos are sorted by min_qty descending, we want to revert such
        order so we get the very first one, which is probably the one to go.
        """
        sellers = super()._prepare_sellers(params)
        if self.env.context.get("override_min_qty"):
            sellers = sellers.sorted("min_qty")
        return sellers

    def _get_supplierinfo_pricelist_price(self, rule, date=None, quantity=None):
        return self.product_tmpl_id._get_supplierinfo_pricelist_price(
            rule, date=date, quantity=quantity, product_id=self.id
        )

    def _price_compute(
        self, price_type, uom=None, currency=None, company=None, date=False
    ):
        if price_type == "supplierinfo":
            prices = dict.fromkeys(self.ids, 0.0)
            rule = self.env["product.pricelist.item"].browse(
                self.env.context.get("supplierinfo_rule")
            )
            for product in self:
                # Use sudo due to avoid access error to public user in e-commerce
                prices[product.id] = product.sudo()._get_supplierinfo_pricelist_price(
                    rule,
                    date=date or self.env.context.get("date", fields.Date.today()),
                    quantity=self.env.context.get("supplierinfo_quantity", 1),
                )
            return prices
        return super()._price_compute(
            price_type,
            uom=uom,
            currency=currency,
            company=company,
            date=date,
        )
