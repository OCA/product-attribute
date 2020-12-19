# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    applied_on = fields.Selection(
        compute="_compute_applied_on", readonly=False, store=True
    )

    @api.depends("product_id")
    def _compute_applied_on(self):
        for record in self:
            # make applied_on consistent (work with manual input and import)
            if record.product_id:
                record.applied_on = "0_product_variant"
            elif not record.product_id and record.product_tmpl_id:
                record.applied_on = "1_product"
