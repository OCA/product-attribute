from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Stored One2many for direct template-level packaging management
    packaging_ids = fields.One2many(
        "product.uom.packaging",
        "product_tmpl_id",
        string="Packaging Configurations",
        help="Packaging configurations for this product template.",
    )
