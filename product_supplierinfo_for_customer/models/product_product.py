# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import datetime

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        if not self.env.context.get("customerinfo"):
            return super().name_get()
    
        # Copied from Odoo with following changes:
        # s/supplier/customer
        # s/seller/buyer
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = '[%s] %s' % (code,name)
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []
        company_id = self.env.context.get('company_id')

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []

        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        # Use `load=False` to not call `name_get` for the `product_tmpl_id`
        self.sudo().read(['name', 'default_code', 'product_tmpl_id'], load=False)
        product_template_ids = self.sudo().mapped('product_tmpl_id').ids

        if partner_ids:
            customer_info = self.env['product.customerinfo'].sudo().search([
                ('product_tmpl_id', 'in', product_template_ids),
                ('partner_id', 'in', partner_ids),
            ])
            # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
            # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
            customer_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
            customer_info_by_template = {}
            for r in customer_info:
                customer_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
        for product in self.sudo():
            variant = product.product_template_attribute_value_ids._get_combination_name()

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            buyers = self.env['product.customerinfo'].sudo().browse(self.env.context.get('buyer_id')) or []
            if not buyers and partner_ids:
                product_customer_info = customer_info_by_template.get(product.product_tmpl_id, [])
                buyers = [x for x in product_customer_info if x.product_id and x.product_id == product]
                if not buyers:
                    buyers = [x for x in product_customer_info if not x.product_id]
                # Filter out sellers based on the company. This is done afterwards for a better
                # code readability. At this point, only a few sellers should remain, so it should
                # not be a performance issue.
                if company_id:
                    buyers = [x for x in buyers if x.company_id.id in [company_id, False]]
            if buyers:
                for s in buyers:
                    buyer_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': buyer_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result

    def _get_price_from_customerinfo(self, partner_id):
        self.ensure_one()
        if not partner_id:
            return 0.0
        partner = self.env["res.partner"].browse(partner_id)
        customerinfo = self._select_customerinfo(partner=partner)
        if customerinfo:
            return customerinfo.price
        return 0.0

    def price_compute(
        self, price_type, uom=False, currency=False, company=None, date=False
    ):
        if price_type == "partner":
            partner_id = self.env.context.get(
                "partner_id", False
            ) or self.env.context.get("partner", False)
            if partner_id and isinstance(partner_id, models.BaseModel):
                partner_id = partner_id.id
            prices = super().price_compute(
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
        return super().price_compute(price_type, uom, currency, company, date=date)

    def _prepare_domain_customerinfo(self, params):
        self.ensure_one()
        partner_id = params.get("partner_id")
        return [
            ("partner_id", "=", partner_id),
            "|",
            ("product_id", "=", self.id),
            "&",
            ("product_tmpl_id", "=", self.product_tmpl_id.id),
            ("product_id", "=", False),
        ]

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
        res = (
            self.env["product.customerinfo"]
            .search(domain)
            .sorted(lambda s: (s.sequence, s.min_qty, s.price, s.id))
        )
        res_1 = res.sorted("product_tmpl_id")[:1]
        return res_1
