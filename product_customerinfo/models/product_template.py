# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.misc import unique


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_ids = fields.One2many(
        comodel_name="product.customerinfo",
        inverse_name="product_tmpl_id",
        string="Customer",
    )

    variant_customer_ids = fields.One2many(
        comodel_name="product.customerinfo",
        inverse_name="product_tmpl_id",
        string="Variant Customer",
    )

    @api.depends_context("display_default_code", "company_id", "partner_id")
    def _compute_display_name(self):
        def get_display_name(name, code):
            if self._context.get("display_default_code", True) and code:
                return f"[{code}] {name}"
            return name

        super()._compute_display_name()
        partner_id = self._context.get("partner_id")
        if not partner_id:
            return
        partner_ids = [
            partner_id,
            self.env["res.partner"].browse(partner_id).commercial_partner_id.id,
        ]
        company_id = self.env.context.get("company_id")

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access("read")

        product_template_ids = self.sudo().ids
        supplier_info_by_template = {}
        if partner_ids:
            # prefetch the fields used by the `display_name`
            domain = [
                ("product_tmpl_id", "in", product_template_ids),
                ("product_id", "=", False),
                ("partner_id", "in", partner_ids),
            ]
            if company_id:
                domain.append(("company_id", "in", [company_id, False]))
            supplier_info = (
                self.env["product.customerinfo"]
                .sudo()
                .search_fetch(
                    domain,
                    ["product_tmpl_id", "company_id", "product_name", "product_code"],
                )
            )
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)

        for product_template in self.sudo():
            name = product_template.name
            product_supplier_info = (
                supplier_info_by_template.get(product_template) or []
            )
            if product_supplier_info:
                temp = []
                for s in product_supplier_info:
                    temp.append(
                        get_display_name(
                            s.product_name or name,
                            s.product_code or product_template.default_code,
                        )
                    )
                # => Feature drop here,
                # one record can only have one display_name now,
                # instead separate with `,`
                product_template.display_name = ", ".join(unique(temp))

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
        match_domain = [("customer_ids", "any", customer_domain)]
        products = self.search_fetch(
            expression.AND([args or [], match_domain]), ["display_name"], limit=limit
        )
        return res + [(product.id, product.display_name) for product in products.sudo()]
