from odoo import fields, models

USAGE_HELP = (
    "Standard categories can be reserved for pricing policy and secondary"
    "ones for catalog management or any other purpose.\n"
)


class ProductCategory(models.Model):
    _inherit = "product.category"

    usage = fields.Selection(
        selection=[("standard", "Standard"), ("secondary", "Secondaire")],
        default="standard",
        help=USAGE_HELP
        + "Secondary categories are displayed in an other field of the product",
    )
