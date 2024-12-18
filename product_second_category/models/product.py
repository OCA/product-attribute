from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_second_id = fields.Many2one(
        comodel_name="product.category",
        domain="[('usage', '=', 'secondary')]",
        string="Categ. Secondaire",
    )
