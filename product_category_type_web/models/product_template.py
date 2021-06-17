from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_web_ids = fields.Many2many(
        comodel_name="product.category",
        domain=[("type", "=", "web")],
        string="Web categories",
    )
