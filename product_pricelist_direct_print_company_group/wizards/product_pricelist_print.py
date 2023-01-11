# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductPricelistPrintCompanyGroup(models.TransientModel):
    _inherit = "product.pricelist.print"

    @api.model
    def _get_sale_order_domain(self, partner):
        domain = super()._get_sale_order_domain(partner)
        if partner.company_group_member_ids:
            origin_domain = ("partner_id", "child_of", partner.id)
            pos = 0
            if origin_domain in domain:
                pos = domain.index(origin_domain)
                domain.remove(origin_domain)
            domain.insert(
                pos, ("partner_id", "in", partner.company_group_member_ids.ids)
            )
        return domain
