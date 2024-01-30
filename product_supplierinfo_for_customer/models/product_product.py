# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import api, fields, models
from odoo.osv import expression
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
        res_ids = list(res)
        res_ids_len = len(res_ids)
        if not limit or res_ids_len >= limit:
            limit = (limit - res_ids_len) if limit else False
        if (
            not name
            and limit
            or not self._context.get("partner_id")
            or res_ids_len >= limit
        ):
            return res_ids
        limit -= res_ids_len
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
            return res_ids
        res_templates = self.browse(res_ids).mapped("product_tmpl_id")
        product_tmpls = (
            self.env["product.customerinfo"]
            .browse(customerinfo_ids)
            .mapped("product_tmpl_id")
            - res_templates
        )
        product_ids = list(
            self._search(
                [("product_tmpl_id", "in", product_tmpls.ids)],
                limit=limit,
                access_rights_uid=name_get_uid,
            )
        )
        res_ids.extend(product_ids)
        return res_ids

    def _get_price_from_customerinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        partner = self.env["res.partner"].browse(partner_id)
        customerinfo = self._select_customerinfo(partner=partner)
        if customerinfo:
            return customerinfo.price
        return 0.0

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        if price_type == "partner":
            partner_id = self.env.context.get(
                "partner_id", False
            ) or self.env.context.get("partner", False)
            if partner_id and isinstance(partner_id, models.BaseModel):
                partner_id = partner_id.id
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

    def _prepare_customers(self, params=False):
        return self.env["product.customerinfo"].search(
            params.get("domain", []),
            order="sequence, min_qty desc, price, id",
        )

    def _prepare_domain_customerinfo(self, params):
        self.ensure_one()
        date = fields.Date.to_string(
            params.get("date") or fields.Date.context_today(self)
        )
        domain = [
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.env.company.id),
            "|",
            ("product_id", "=", self.id),
            "&",
            ("product_tmpl_id", "=", self.product_tmpl_id.id),
            ("product_id", "=", False),
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", date),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", date),
        ]
        partner_id = params.get("partner_id")
        if partner_id:
            domain = expression.AND(
                [domain, [("name", "in", (partner_id + partner_id.parent_id).ids)]]
            )
        return domain

    def _customers_filter_by_quantity(self, customers, quantity, uom_id, precision):
        res = self.env["product.customerinfo"]
        # Set quantity in UoM of customer
        if quantity:
            if uom_id and self.uom_id and uom_id != self.uom_id:
                quantity = uom_id._compute_quantity(quantity, self.uom_id)
        for customer in customers:
            if quantity:
                if (
                    float_compare(
                        quantity,
                        customer.min_qty,
                        precision_digits=precision,
                    )
                    == -1
                ):
                    continue
            else:
                if customer.min_qty:
                    continue
            res |= customer
        return res

    def _select_customerinfo(
        self, partner=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        """
        Customer version of the standard `_select_seller`.
        If you want not to filter by quantity, explicitly pass quantity=None
        """
        self.ensure_one()
        if not params:
            params = {}
        params.update({"date": date, "partner_id": partner})
        domain = self._prepare_domain_customerinfo(params)
        params["domain"] = domain

        customerinfos = self._prepare_customers(params)
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )

        if quantity is not None:
            customerinfos = self._customers_filter_by_quantity(
                customerinfos, quantity=quantity, uom_id=uom_id, precision=precision
            )
        if customerinfos:
            customer = customerinfos[0].name
            customerinfos = customerinfos.filtered(
                lambda x, name=customer: x.name == name
            )

        # Prefer matching specific variants over templates if possible
        variant_res = customerinfos.filtered(lambda x: x.product_id)
        if variant_res:
            customerinfos = variant_res

        return customerinfos.sorted("price")[:1]
