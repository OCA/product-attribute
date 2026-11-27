from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    avg_cost = fields.Monetary(groups="product_cost_security.group_product_cost")
    total_value = fields.Monetary(groups="product_cost_security.group_product_cost")
