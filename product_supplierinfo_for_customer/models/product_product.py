# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import api, models


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
        customerinfo = self.env["product.customerinfo"].search(
            [
                ("name", "=", partner_id),
                "|",
                ("product_id", "=", self.id),
                "&",
                ("product_tmpl_id", "=", self.product_tmpl_id.id),
                ("product_id", "=", False),
            ],
            limit=1,
            order="product_id, sequence",
        )
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
