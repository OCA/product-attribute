# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import api, fields, models
from odoo.tools import float_compare


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        res = super(ProductProduct, self.with_context(customerinfo=True)).name_get()
        return res

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        res = super(ProductProduct, self)._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
        if not limit or len(res) >= limit:
            limit = (limit - len(res)) if limit else False
        if (
            not name
            and limit
            or not self._context.get("partner_id")
            or len(res) >= limit
        ):
            return res
        limit -= len(res)
        customerinfo_ids = self.env["product.customerinfo"]._search(
            [
                ("name", "=", self._context.get("partner_id")),
                "|",
                ("product_code", operator, name),
                ("product_name", operator, name),
            ],
            limit=limit,
            access_rights_uid=name_get_uid,
        )
        if not customerinfo_ids:
            return res
        res_templates = self.browse([product_id for product_id, _name in res]).mapped(
            "product_tmpl_id"
        )
        product_tmpls = (
            self.env["product.customerinfo"]
            .browse(customerinfo_ids)
            .mapped("product_tmpl_id")
            - res_templates
        )
        product_ids = self._search(
            [("product_tmpl_id", "in", product_tmpls.ids)],
            limit=limit,
            access_rights_uid=name_get_uid,
        )
        res.extend(self.browse(product_ids).name_get())
        return res

    def _get_price_from_customerinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        customerinfo = self._select_customerinfo(partner_id=partner_id)
        if customerinfo:
            return customerinfo.price
        return 0.0

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        if price_type == "partner":
            partner_id = self.env.context.get(
                "partner_id", False
            ) or self.env.context.get("partner", False)
            if partner_id and isinstance(partner_id, int):
                partner_id = self.env["res.partner"].browse(partner_id)
            prices = super(ProductProduct, self).price_compute(
                "list_price", uom, currency, company
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
        return super(ProductProduct, self).price_compute(
            price_type, uom, currency, company
        )

    def _prepare_customerinfo(self, params):
        # This search is made to avoid retrieving from the cache.
        return (
            self.env["product.customerinfo"]
            .search(
                [
                    ("product_tmpl_id", "=", self.product_tmpl_id.id),
                    ("name.active", "=", True),
                ]
            )
            .sorted(lambda s: (s.sequence, -s.min_qty, s.price, s.id))
        )

    def _select_customerinfo(
        self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        """Customer version of the standard `_select_seller`.
        """
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )

        res = self.env["product.customerinfo"]
        customers = self._prepare_customerinfo(params)
        if self.env.context.get("force_company"):
            customers = customers.filtered(
                lambda s: not s.company_id
                or s.company_id.id == self.env.context["force_company"]
            )
        for customer in customers:
            quantity_uom_customer = quantity
            if quantity_uom_customer and uom_id and uom_id != customer.product_uom:
                quantity_uom_customer = uom_id._compute_quantity(
                    quantity_uom_customer, customer.product_uom
                )

            if customer.date_start and customer.date_start > date:
                continue
            if customer.date_end and customer.date_end < date:
                continue
            if (
                float_compare(
                    quantity_uom_customer, customer.min_qty, precision_digits=precision
                )
                == -1
            ):
                continue
            if partner_id and customer.name not in [partner_id, partner_id.parent_id]:
                continue
            if customer.product_id and customer.product_id != self:
                continue
            if not res or res.name == customer.name:
                res |= customer
        # NOTE: This differs from the standard sellers logic. This is done to
        # keep the old behavior of this module.
        variant_specific = res.filtered(lambda r: r.product_id)
        if variant_specific:
            res = variant_specific
        return res.sorted("price")[:1]
