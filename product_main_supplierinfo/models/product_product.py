# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    main_seller_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Main Vendor",
        compute="_compute_main_seller_id",
    )

    @api.depends(
        "seller_ids.partner_id.active",
        "seller_ids.sequence",
        "seller_ids.min_qty",
        "seller_ids.price",
        "seller_ids.company_id",
        "seller_ids.product_id",
        "seller_ids.date_start",
        "seller_ids.date_end",
    )
    @api.depends_context("company")
    def _compute_main_seller_id(self):
        for product in self.with_context(compute_main_seller=True):
            product.main_seller_id = fields.first(
                product._get_filtered_sellers(quantity=None).sorted("price")
            )

    def _get_filtered_sellers(
        self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        res = super()._get_filtered_sellers(partner_id, quantity, date, uom_id, params)
        if not res and self.env.context.get("compute_main_seller"):
            sellers_filtered = self._prepare_sellers(params)
            sellers_filtered = sellers_filtered.filtered(
                lambda s: not s.company_id or s.company_id.id == self.env.company.id
            )
            res = sellers_filtered.filtered(lambda s: s.product_id == self)
        return res
