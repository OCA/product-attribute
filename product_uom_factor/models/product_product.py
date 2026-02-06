from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    uom_factor_ids = fields.Many2many(
        "product.uom.factor",
        string="UoM Conversion Factors",
        compute="_compute_uom_factor_ids",
    )

    def _compute_uom_factor_ids(self):
        Factor = self.env["product.uom.factor"]
        for product in self:
            if not product.id or not product.product_tmpl_id.id:
                product.uom_factor_ids = Factor
                continue
            product.uom_factor_ids = Factor.search(
                [
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                    "|",
                    ("product_ids", "=", False),
                    ("product_ids", "in", product.id),
                ]
            )
