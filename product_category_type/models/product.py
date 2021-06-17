from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    type = fields.Selection(selection=[("base", "Base")], default="base", required=True)
