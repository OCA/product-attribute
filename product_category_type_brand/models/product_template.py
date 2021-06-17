from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_brand_id = fields.Many2one(
        comodel_name="product.category",
        domain=[
            ("type", "=", "brand"),
        ],
        string="Brand",
    )
