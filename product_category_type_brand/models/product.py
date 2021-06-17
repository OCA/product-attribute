from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    type = fields.Selection(
        selection_add=[("brand", "Brand")],
        ondelete={"brand": lambda recs: recs.write({"type": "base"})},
    )
    brand_product_count = fields.Integer(
        "# Products",
        compute="_compute_brand_product_count",
        help="The number of products under this brand (Does not consider the children brand)",
    )

    def _compute_brand_product_count(self):
        read_group_res = self.env["product.template"].read_group(
            [("categ_brand_id", "child_of", self.ids)],
            ["categ_brand_id"],
            ["categ_brand_id"],
        )
        group_data = {
            data["categ_brand_id"][0]: data["categ_brand_id_count"]
            for data in read_group_res
        }
        for categ in self:
            brand_product_count = 0
            for sub_categ_id in categ.search([("id", "child_of", categ.ids)]).ids:
                brand_product_count += group_data.get(sub_categ_id, 0)
            categ.brand_product_count = brand_product_count
