from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    usage = fields.Selection(
        selection=[("standard", "Standard"), ("secondary", "Secondaire")],
        default="standard",
    )
