# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from collections import Counter

from odoo import api, models
from odoo.exceptions import UserError


class StockLot(models.Model):
    _inherit = "stock.lot"

    def _check_lot_name_unique(self):
        """Refuse a name another product of the same company already holds"""
        if not self:
            return
        # allow duplicates from module installs, like mrp_workorder demo data
        if self.env.context.get("install_module"):
            return
        if self.env.user.has_group(
            "stock_lot_unique_name.group_allow_duplicate_lot_name"
        ):
            return
        # company_id is optional on a lot, so pair it with the name in python
        # rather than in the domain, where a missing company matches nothing
        counts = Counter((lot.name, lot.company_id.id) for lot in self)
        # catch clashes from the create call as well
        clashing = {name for (name, _company), count in counts.items() if count > 1}
        clashing.update(
            # a record rule hiding the other lot would otherwise let it through;
            # only names the user just submitted are reported back
            self.sudo()
            .search([("id", "not in", self.ids), ("name", "in", self.mapped("name"))])
            .filtered(lambda lot: (lot.name, lot.company_id.id) in counts)
            .mapped("name")
        )
        if clashing:
            raise UserError(
                self.env._(
                    "The lot or serial numbers %(names)s are used by more than"
                    " one product.",
                    names=sorted(clashing),
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        lots = super().create(vals_list)
        lots._check_lot_name_unique()
        return lots

    def write(self, vals):
        result = super().write(vals)
        if "name" in vals or "company_id" in vals:
            self._check_lot_name_unique()
        return result
