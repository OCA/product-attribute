# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(
        compute="_compute_applied_on",
        readonly=False,
        store=True,
    )

    @api.depends("product_id", "product_tmpl_id")
    def _compute_applied_on(self):
        # make applied_on consistent with manual input
        for record in self:
            if record.product_id:
                record.applied_on = "0_product_variant"
            elif record.product_tmpl_id:
                record.applied_on = "1_product"

    @api.model
    def _add_missing_default_values(self, values):
        # make applied_on consistent during import
        if values.get("product_id"):
            values["applied_on"] = "0_product_variant"
        elif values.get("product_tmpl_id"):
            values["applied_on"] = "1_product"
        return super()._add_missing_default_values(values)
