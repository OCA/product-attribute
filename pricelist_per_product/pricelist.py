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
    def _compute_count_products(self):
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
        compute='_compute_count_products',
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
        related="sequence",
        help="Allows to modify the sequence manually because "
             "the sequence field is difficult to modify because 'handle'.")

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
    def _get_sequence_price_grid(self, vals):
        """
            In sale order line, we want to use as a priority
            the product pricelist item associated with the product variant.
            But in Odoo, it's the product pricelist item which has the
            smallest sequence that is used.
            That's why, we put a smaller sequence to the product pricelist item
            of the product variant and a larger sequence to
            the product pricelist item of the product template.
        """
        product_id = vals.get('product_id', self.product_id)
        product_tmpl_id = vals.get('product_tmpl_id', self.product_tmpl_id)
        related_sequence = 15
        if product_id:
            related_sequence = 5
        elif product_tmpl_id:
            related_sequence = 10
        return related_sequence

    @api.model
    def create(self, vals):
        if not self._is_catch_all_item(vals) and \
                self.env['product.pricelist.version'].browse(
                    vals['price_version_id']).price_grid:
            vals.update({
                'price_discount': -1,
                'related_sequence': self._get_sequence_price_grid(vals),
                'base': vals.get('base', 1),
            })
        return super(ProductPricelistItem, self).create(vals)

    @api.multi
    def write(self, vals):
        for item in self:
            if not self._is_catch_all_item(vals) and 'product_id' in vals:
                vals['related_sequence'] = item._get_sequence_price_grid(
                    vals)
            super(ProductPricelistItem, item).write(vals)
        return True

    @api.model
    def _is_catch_all_item(self, vals):
        """ Sale Pricelists require a pricelist item in order to work.
            This item must be based on public price without discount/surcharge
            If not, public price from product is not propagated in sale line
            and price is 0.0
            Here we don't want block this behavior.
        """
        values = vals.copy()
        conditions = {
            'min_quantity': 0,
            'price_surcharge': 0,
            'price_discount': 0,
            'categ_id': False,
            'product_id': False,
            'product_tmpl_id': False,
        }
        # We complete missing keys in values dict
        # (write could have less keys than create)
        for key in conditions.keys():
            if key not in values:
                values[key] = self[key] or False  # value in db
        # we check 1 condition which prevent to be a catchall
        for key, elm in conditions.items():
            if key in values and values.get(key) != elm:
                return False
        return True
