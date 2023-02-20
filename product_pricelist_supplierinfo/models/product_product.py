# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.tools import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_supplierinfo_pricelist_price(self, rule, date=None, quantity=None):
        return self.product_tmpl_id._get_supplierinfo_pricelist_price(
            rule, date=date, quantity=quantity, product_id=self.id
        )

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == "supplierinfo":
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company
        )

    def _get_select_seller_params(
        self, rule=None, date=None, quantity=0.0, product_id=None
    ):
        return self.product_tmpl_id._get_select_seller_params(
            rule, date=date, quantity=quantity, product_id=self.id
        )

    def _prepare_sellers(self, params):
        sellers = super()._prepare_sellers(params=params)
        if self.env.context.get("override_min_qty"):
            # When we override min qty we want that _select_sellers gives us the
            # first possible seller for every other criteria ignoring the quantity. As
            # supplierinfos are sorted by min_qty descending, we want to revert such
            # order so we get the very first one, which is probably the one to go.
            sellers = sellers.sorted("min_qty")

        # inherited _prepare_sellers method makes a sort by
        # (s.sequence, -s.min_qty, s.price, s.id) but it does
        # not consider currency conversion. We convert to
        # pricelist currency (or company curr if not found)
        # when needed and sort again
        if isinstance(params, dict) and params.get("convert_currencies"):
            company = params.get("company") or self.env.company
            to_currency = params.get("pricelist_currency")
            if not to_currency:
                # pricelist currency has priority
                to_currency = self.env.company.currency_id
            sellers = sellers.sorted(
                key=lambda s: (
                    s.currency_id._convert(
                        from_amount=s.price,
                        to_currency=to_currency,
                        company=company,
                        date=fields.Date.today(),
                    )
                ),
                reverse=False,
            )
            # reverse False will keep order by price ascendant
        return sellers

    def _select_seller(
        self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        """@override: propagate params to _prepare_seller method if needed"""

        res = super()._select_seller(
            partner_id=partner_id,
            quantity=quantity,
            date=date,
            uom_id=uom_id,
            params=params,
        )

        if isinstance(params, dict) and params.get("convert_currencies"):
            # re-execute flow and propagate param to _prepare_seller
            self.ensure_one()
            if date is None:
                date = fields.Date.context_today(self)
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )

            res = self.env["product.supplierinfo"]
            sellers = self._prepare_sellers(params)
            sellers = sellers.filtered(
                lambda s: not s.company_id or s.company_id.id == self.env.company.id
            )
            for seller in sellers:
                # Set quantity in UoM of seller
                quantity_uom_seller = quantity
                if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                    quantity_uom_seller = uom_id._compute_quantity(
                        quantity_uom_seller, seller.product_uom
                    )

                if seller.date_start and seller.date_start > date:
                    continue
                if seller.date_end and seller.date_end < date:
                    continue
                if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                    continue
                if (
                    quantity is not None
                    and float_compare(
                        quantity_uom_seller, seller.min_qty, precision_digits=precision
                    )
                    == -1
                ):
                    continue
                if seller.product_id and seller.product_id != self:
                    continue
                if not res or res.name == seller.name:
                    res |= seller
            return res.sorted("price")[:1]

        # return sellers as they were ordered, if no convert param
        return res
