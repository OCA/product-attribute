from openerp import models, api, fields, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    price_history_count = fields.Integer(
        "Price History Count", compute='_compute_price_history_count')

    @api.multi
    def _compute_price_history_count(self):
        for p in self:
            p.price_history_count = self.env['product.price.history']\
                .search_count([
                    ('product_template_id', '=', p.product_tmpl_id.id),
                ])

    @api.multi
    def action_product_price_history_view(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx["search_default_product_template_id"] = self.product_tmpl_id.id
        return {
            'name': _('Product Price History'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'res_model': 'product.price.history',
            'target': 'current',
            'context': ctx,
        }
