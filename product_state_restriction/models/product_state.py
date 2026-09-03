# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    restrict_sale = fields.Boolean(
        string="Restrict Sales",
        help="Products in this state cannot be sold (sale_ok = False).",
    )

    restrict_manufacture = fields.Boolean(
        string="Restrict Manufacturing",
        help="Products in this state cannot be manufactured / used as components.",
    )

    restrict_outgoing = fields.Boolean(
        string="Restrict Outgoing Moves",
        help="Products in this state cannot leave the warehouse.",
    )

    def write(self, vals):
        res = super().write(vals)
        if "restrict_sale" in vals:
            self._sync_sale_ok_on_products()
        return res

    def _sync_sale_ok_on_products(self):
        """Update sale_ok on all products that currently use these states."""
        for state in self:
            products = state.product_ids
            if products:
                products.write({"sale_ok": not state.restrict_sale})
