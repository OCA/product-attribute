from odoo import fields, models

from .product_category import USAGE_HELP


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_second_id = fields.Many2one(
        comodel_name="product.category",
        domain="[('usage', '=', 'secondary')]",
        string="Secondary Category",
        help="This field also displays product categories but only "
        "'secondary' ones.\n"
        "Such a category type can be defined with the 'usage' "
        "field on the categories" + USAGE_HELP,
    )
