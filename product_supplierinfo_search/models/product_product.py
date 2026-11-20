# Copyright 2026 Jarsa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.fields import Domain


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _supplierinfo_search_domain(self, operator, value):
        return Domain(
            [
                "|",
                ("product_code", operator, value),
                ("product_name", operator, value),
            ]
        )

    @api.model
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        res = super().name_search(name, domain, operator, limit)
        # Core already searches supplier code/name as a last hope when a
        # supplier is in the context; only extend the search when it isn't.
        if not name or self.env.context.get("partner_id"):
            return res
        if operator in Domain.NEGATIVE_OPERATORS:
            return res
        limit_rest = limit and limit - len(res)
        if limit_rest is not None and limit_rest <= 0:
            return res
        match_domain = Domain(
            "product_tmpl_id.seller_ids",
            "any",
            self._supplierinfo_search_domain(operator, name),
        )
        products = self.search_fetch(
            Domain(domain or Domain.TRUE)
            & Domain("id", "not in", [r[0] for r in res])
            & match_domain,
            ["display_name"],
            limit=limit_rest or None,
        )
        return res + [(p.id, p.display_name) for p in products.sudo()]

    @api.model
    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        # Same idea for generic display_name domain searches (filter panels,
        # explicit domains), which take a different ORM entry point.
        if not value or self.env.context.get("partner_id"):
            return domain
        supplier_match = [
            (
                "product_tmpl_id.seller_ids",
                "any",
                self._supplierinfo_search_domain(operator, value),
            )
        ]
        # ponytail: mirror core's negative-operator handling (AND) vs positive
        # (OR); refining NOT-semantics on supplier names is an edge case.
        if operator in Domain.NEGATIVE_OPERATORS:
            return Domain.AND([domain, supplier_match])
        return Domain.OR([domain, supplier_match])
