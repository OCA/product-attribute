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
        )
        if not sellers:
            sellers = all_sellers.filtered(lambda s: (s.product_id == self))
            if not sellers:
                sellers = all_sellers.filtered(lambda s: not s.product_id)
        return sellers.sorted("price")
