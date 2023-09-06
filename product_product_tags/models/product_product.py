# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductProduct(models.Model):
    """Goal of this class is to handle variant tag mngmt without affecting product tmpl"""

    _inherit = "product.product"

    var_tag_ids = fields.Many2many(
        comodel_name="product.template.tag",
        relation="product_variant_var_tag_rel",
        column1="product_id",
        column2="tag_id",
        string="Variant Tags",
        help="Product variant tags",
    )

    @api.model
    def create(self, vals):
        if type(dict):
            vals = [vals]
        for value in vals:
            product_tmpl_id = value.get("product_tmpl_id")
            if product_tmpl_id:
                product_template = self.env["product.template"].browse(product_tmpl_id)
                tag_ids = product_template.tag_ids.ids
                if tag_ids:
                    value["var_tag_ids"] = [(6, 0, tag_ids)]
        return super().create(vals)
