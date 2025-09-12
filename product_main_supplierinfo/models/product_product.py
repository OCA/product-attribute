# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    main_seller_id = fields.Many2one(
        comodel_name="product.supplierinfo",
        string="Main Vendor",
        compute="_compute_main_seller_id",
        search="_search_main_seller_id",
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
        for product in self:
            sellers = product._get_sellers()
            product.main_seller_id = fields.first(sellers)

    def _search_main_seller_id(self, operator, value):
        seller_obj = self.env["product.supplierinfo"]
        # Search all sellers matching the partner criteria
        sellers = seller_obj.search([("partner_id", operator, value)])
        # Get all products having one of these sellers as main seller
        products = sellers.product_tmpl_id.product_variant_id
        products = products.filtered(lambda p: p.main_seller_id in sellers)
        return [("id", "in", products.ids)]

    def _get_sellers(self):
        """Returns all available sellers of a product based on some constraints.

        They are ordered and filtered like it is done in the standard 'product' addon.
        """
        self.ensure_one()
        all_sellers = self._prepare_sellers(False).filtered(
            lambda s: not s.company_id or s.company_id.id == self.env.company.id
        )
        today = fields.Date.context_today(self)
        sellers = all_sellers.filtered(
            lambda s: (
                (s.product_id == self or not s.product_id)
                and (
                    (s.date_start <= today if s.date_start else True)
                    and (s.date_end >= today if s.date_end else True)
                )
            )
        )
        if not sellers:
            sellers = all_sellers.filtered(lambda s: (s.product_id == self))
            if not sellers:
                sellers = all_sellers.filtered(lambda s: not s.product_id)
        return sellers.sorted("price")
