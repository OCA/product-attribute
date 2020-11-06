# Copyright 2020 Andrea Piovesana (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields

class ProductPriceHistory(models.Model):
    _inherit = 'product.price.history'

    product_tmpl_id = fields.Many2one(string='Product Template', store=True, related='product_id.product_tmpl_id')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_history_count = fields.Integer("Price History Count", compute='compute_price_history_count')

    @api.one
    def compute_price_history_count(self):
        self.price_history_count = self.env['product.price.history'].search_count([('product_tmpl_id', '=', self.id)])
        #self.price_history_count = self.env['product.price.history'].search_count([('product_id', '=', self.product_variant_ids[0].id)])


class ProductProduct(models.Model):
    _inherit = 'product.product'

    price_history_count = fields.Integer("Price History Count", compute='compute_price_history_count')

    @api.one
    def compute_price_history_count(self):
        self.price_history_count = self.env['product.price.history'].search_count([('product_id', '=', self.id)])


