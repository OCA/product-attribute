# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.fields import Domain


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_domain_customerinfo(self, params):
        self.ensure_one()
        partner_id = params.get("partner_id")
        domain = Domain.OR(
            [
                Domain("product_id", "=", self.id),
                Domain.AND(
                    [
                        Domain("product_tmpl_id", "=", self.product_tmpl_id.id),
                        Domain("product_id", "=", False),
                    ]
                ),
            ]
        )
        if partner_id:
            # Restrict to this exact partner: the fallback across hierarchy
            # levels (client, parent company, company group) is handled by
            # ``_select_customerinfo``, one level at a time, so that a match
            # on a more specific level always wins over a less specific one.
            domain &= Domain("partner_id", "=", partner_id)
        return domain

    def _get_customerinfo_partner_hierarchy(self, partner):
        """Return the partners to check for customerinfo, in order of
        precedence: the client itself, its parent company, then its company
        group (``company_group_id``, from ``base_partner_company_group``).
        """
        partner_ids = []
        for candidate_id in (
            partner.id,
            partner.parent_id.id,
            partner.company_group_id.id,
        ):
            if candidate_id and candidate_id not in partner_ids:
                partner_ids.append(candidate_id)
        return self.env["res.partner"].browse(partner_ids)

    def _select_customerinfo(
        self, partner=False, _quantity=0.0, _date=None, _uom_id=False, params=False
    ):
        if not partner:
            return super()._select_customerinfo(
                partner=partner,
                _quantity=_quantity,
                _date=_date,
                _uom_id=_uom_id,
                params=params,
            )
        for candidate in self._get_customerinfo_partner_hierarchy(partner):
            customerinfo = super()._select_customerinfo(
                partner=candidate,
                _quantity=_quantity,
                _date=_date,
                _uom_id=_uom_id,
                params=params,
            )
            if customerinfo:
                return customerinfo
        return self.env["product.customerinfo"].browse()
