# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import api, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_display_name(self):
        return super(
            ProductProduct, self.with_context(customerinfo=True)
        )._compute_display_name()

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        res = super().name_search(name, args=args, operator=operator, limit=limit)
        res_ids_len = len(res)
        if (
            not name
            and limit
            or not self._context.get("partner_id")
            or res_ids_len >= limit
        ):
            return res
        limit -= res_ids_len
        customer_domain = self.env["product.customerinfo"]._get_name_search_domain(
            self._context.get("partner_id"), operator, name
        )
        match_domain = [("product_tmpl_id.customer_ids", "any", customer_domain)]
        products = self.search_fetch(
            expression.AND([args or [], match_domain]), ["display_name"], limit=limit
        )
        return res + [(product.id, product.display_name) for product in products.sudo()]

    def _get_price_from_customerinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        partner = self.env["res.partner"].browse(partner_id)
        customerinfo = self._select_customerinfo(partner=partner)
        if customerinfo:
            return customerinfo.price
        return 0.0

    def _price_compute(
        self, price_type, uom=False, currency=False, company=None, date=False
    ):
        if price_type == "partner":
            partner_id = self.env.context.get(
                "partner_id", False
            ) or self.env.context.get("partner", False)
            if partner_id and isinstance(partner_id, models.BaseModel):
                partner_id = partner_id.id
            prices = super()._price_compute(
                "list_price", uom, currency, company, date=date
            )
            for product in self:
                price = product._get_price_from_customerinfo(partner_id)
                if not price:
                    continue
                prices[product.id] = price
                if not uom and self._context.get("uom"):
                    uom = self.env["uom.uom"].browse(self._context["uom"])
                if not currency and self._context.get("currency"):
                    currency = self.env["res.currency"].browse(
                        self._context["currency"]
                    )
                if uom:
                    prices[product.id] = product.uom_id._compute_price(
                        prices[product.id], uom
                    )
                if currency:
                    date = self.env.context.get("date", datetime.datetime.now())
                    prices[product.id] = product.currency_id._convert(
                        prices[product.id], currency, company, date
                    )
            return prices
        return super()._price_compute(price_type, uom, currency, company, date=date)

    def _prepare_domain_customerinfo(self, params):
        self.ensure_one()
        partner_id = params.get("partner_id")
        domain = [
            "|",
            ("product_id", "=", self.id),
            "&",
            ("product_tmpl_id", "=", self.product_tmpl_id.id),
            ("product_id", "=", False),
        ]
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            domain = expression.AND(
                [
                    domain,
                    [
                        (
                            "partner_id",
                            "in",
                            (
                                partner
                                + partner.parent_id
                                + partner.commercial_partner_id
                            ).ids,
                        )
                    ],
                ]
            )
        return domain

    def _select_customerinfo(
        self, partner=False, _quantity=0.0, _date=None, _uom_id=False, params=False
    ):
        """Customer version of the standard `_select_seller`."""
        # TODO: For now it is just the function name with same arguments, but
        #  can be changed in future migrations to be more in line Odoo
        #  standard way to select supplierinfo's.
        if not params:
            params = dict()
        params.update({"partner_id": partner.id})
        domain = self._prepare_domain_customerinfo(params)
        # Search for customerinfo records based on the domain
        any_match = self.env["product.customerinfo"].search(
            domain, order="sequence,min_qty,price,id"
        )
        first_template_match = self.env["product.customerinfo"].browse()
        # return the first customer_info matching the variant
        # otherwise the first one matching the template
        for customer_info in any_match:
            if customer_info.product_id == self:
                return customer_info
            if (
                not customer_info.product_id
                and not first_template_match
                and customer_info.product_tmpl_id == self.product_tmpl_id
            ):
                first_template_match = customer_info
        return first_template_match
