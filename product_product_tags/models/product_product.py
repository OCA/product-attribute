# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductProduct(models.Model):
    """Overwriting tag_ids to make it idependant from template after creation"""

    _inherit = "product.product"

    tag_ids = fields.Many2many(
        comodel_name="product.template.tag",
        string="Tags",
        relation="product_variant_var_tag_rel",
        column1="product_id",
        column2="tag_id",
        copy=False,
    )

    @api.model_create_multi
    def create(self, list_vals):
        """Copying tag_ids values from template at creation"""
        for value in list_vals:
            product_tmpl_id = value.get("product_tmpl_id")
            if product_tmpl_id:
                product_template = self.env["product.template"].browse(product_tmpl_id)
                tag_ids = product_template.tag_ids.ids
                if tag_ids:
                    value["tag_ids"] = [(6, 0, tag_ids)]
        return super().create(list_vals)
