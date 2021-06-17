from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    type = fields.Selection(
        selection_add=[("web", "Web")],
        ondelete={"web": lambda recs: recs.write({"type": "base"})},
    )
