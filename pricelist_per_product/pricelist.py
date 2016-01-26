# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


PRICE_GRID_HELP = _("""Define if the price list items are filled
from product form with a grid of specific values
for each product""")


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    price_grid = fields.Boolean(
        string='Product Price Grid',
        help=PRICE_GRID_HELP)


class ProductPricelistVersion(models.Model):
    _inherit = 'product.pricelist.version'

    @api.depends('tmpl_in_count')
    def count_products(self):
        PPItem_m = self.env['product.pricelist.item']
        for record in self:
            if not isinstance(self.id, models.NewId):
                predicats = {
                    'tmpl_in_count': ('product_tmpl_id', '!=', False),
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
    tmpl_in_count = fields.Integer(
        string="Template with this Version",
        compute='count_products',
        help="Number of Product Template with this Pricelist version")
    item_grid_ids = fields.One2many(
        'product.pricelist.item',
        'price_version_id')

    @api.multi
    def button_template_in_version(self):
        self.ensure_one()
        domain = [('pricelist_item_ids.price_version_id', '=', self.id)]
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'view_mode': 'tree,form',
            'res_model': 'product.template',
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
    def button_product(self):
        self.ensure_one()
        if self.product_tmpl_id:
            product = self.product_tmpl_id
        else:
            product = self.product_id.product_tmpl_id
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'name': 'Product',
            'view_mode': 'form',
            'res_id': product.id,
            'res_model': 'product.template',
        }

    @api.model
    def create(self, vals):
        if self.env['product.pricelist.version'].browse(
                vals['price_version_id']).price_grid:
            vals.update({
                'price_discount': -1,
                'sequence': 1,
                'base': 1,
            })
        return super(ProductPricelistItem, self).create(vals)
