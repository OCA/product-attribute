from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    authorized_to_be_sold = fields.Boolean()
    authorized_to_be_bought = fields.Boolean()
