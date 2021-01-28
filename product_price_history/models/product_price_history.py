from odoo import models, fields


class ProductPriceHistory(models.Model):
    _inherit = 'product.price.history'

    product_tmpl_id = fields.Many2one(
        string='Product Template', store=True, related='product_id.product_tmpl_id')
