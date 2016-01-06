# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


PRICE_GRID_HELP = _("""Define if the price list items are filled
from product form with a grid of specific values
for each product""")

HELP_NAME_ON_ACTION = _("Change all your '%s' prices in one time "
                        "by click on 'More' button")


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    price_grid = fields.Boolean(
        string='Product Price Grid',
        help=PRICE_GRID_HELP)


class ProductPricelistVersion(models.Model):
    _inherit = 'product.pricelist.version'

    @api.depends('product_in_count')
    def count_products(self):
        PPItem_m = self.env['product.pricelist.item']
        for record in self:
            if not isinstance(self.id, models.NewId):
                predicats = {
                    'tmpl_in_count': ('product_tmpl_id', '!=', False),
                    'product_in_count': ('product_id', '!=', False),
                }
                version_domain = [('price_version_id', '=', record.id)]
                for field, predicat in predicats.items():
                    domain = list(version_domain)
                    domain.append(predicat)
                    self[field] = PPItem_m.search_count(domain)

    price_grid = fields.Boolean(
        related='pricelist_id.price_grid',
        domain=[('price_surcharge', '=', 0)],
        store=True,
        help=PRICE_GRID_HELP)
    product_in_count = fields.Integer(
        string="Products with this Version",
        compute='count_products',
        help="Number of Product with this Pricelist version")
    tmpl_in_count = fields.Integer(
        string="Template with this Version",
        compute='count_products',
        help="Number of Product Template with this Pricelist version")
    item_grid_ids = fields.One2many(
        'product.pricelist.item',
        'price_version_id')

    @api.multi
    def button_product_in_version(self):
        return (self.goto_products_from_version('product.product', 'in'))

    @api.multi
    def button_product_out_version(self):
        return self.goto_products_from_version('product.product', 'out')

    @api.multi
    def button_template_in_version(self):
        return self.goto_products_from_version('product.template', 'in')

    @api.multi
    def button_template_out_version(self):
        return self.goto_products_from_version('product.template', 'out')

    @api.model
    def goto_products_from_version(self, model, direction):
        if model == 'product.product':
            view_name = 'product'
        else:
            view_name = 'product_template'
        if direction == 'in':
            domain = [('pricelist_item_ids.price_version_id', '=', self.id)]
        else:
            domain = [('pricelist_item_ids.price_version_id', '!=', self.id)]
        action_name = view_name.replace('_', ' ') + 's'
        view_id_ref = 'pricelist_per_product.%s_tree_price_view' % view_name
        ctx = self.env.context.copy()
        ctx['price_version_id'] = self.id
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'name': HELP_NAME_ON_ACTION % action_name,
            'view_mode': 'tree',
            'res_model': model,
            'view_id': self.env.ref(view_id_ref).id,
            'context': ctx
        }


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    date_end = fields.Date(
        related='price_version_id.date_end',
        readonly=True)
    currency_name = fields.Many2one(
        related='price_version_id.pricelist_id.currency_id',
        readonly=True)
    related_sequence = fields.Integer(
        String='Sequence',
        related="sequence")

    @api.multi
    def button_product_product(self):
        return self.goto_product('product.product')

    @api.multi
    def button_product_template(self):
        return self.goto_product('product.template')

    @api.model
    def goto_product(self, model):
        if model == 'product.product':
            product = self.product_id.id
        else:
            product = self.product_tmpl_id.id
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'name': 'Product',
            'view_mode': 'form',
            'res_id': product,
            'res_model': model,
        }
