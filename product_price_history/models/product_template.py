from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_history_count = fields.Integer(
        "Price History Count", compute='_compute_price_history_count')

    @api.multi
    def _compute_price_history_count(self):
        for t in self:
            t.price_history_count = self.env['product.price.history'].search_count(
                [('product_tmpl_id', '=', t.id)])
