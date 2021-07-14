# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.modules.registry import Registry


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    display_pricelist_price = fields.Boolean(
        string="Display in Pricelist Prices",
        help="If marked, this pricelist will be displayed in the product "
        "pricelist prices views.",
    )

    @api.model
    def create(self, vals):
        res = super(Pricelist, self).create(vals)
        if (
            self.env["product.product"]._register_hook()
            or self.env["product.template"]._register_hook()
        ):
            Registry(self.env.cr.dbname).registry_invalidated = True
        return res

    def write(self, vals):
        res = super(Pricelist, self).write(vals)
        if (
            self.env["product.product"]._register_hook()
            or self.env["product.template"]._register_hook()
        ):
            Registry(self.env.cr.dbname).registry_invalidated = True
        return res
