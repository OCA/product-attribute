# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    # Columns Section
    product_variant_count = fields.Integer(
        compute="_compute_product_variant_count", string="Variants Quantity"
    )

    # Compute Section
    def _compute_product_variant_count(self):
        res = {}
        search = self.env["product.product"].read_group([], ["categ_id"], ["categ_id"])
        for item in search:
            res[item["categ_id"][0]] = item["categ_id_count"]
        for category in self:
            category.product_variant_count = res.get(category.id, 0)
