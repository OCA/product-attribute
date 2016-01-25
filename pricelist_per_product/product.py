# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _default_pricelist_item_ids(self):
        return self.default_pricelist_item_ids()

    pricelist_item_ids = fields.One2many(
        'product.pricelist.item',
        'product_tmpl_id',
        string='Pricelist Items',
        default=_default_pricelist_item_ids,
        help="These prices are defined with absolute values\n"
             "(no calculation with discount)"
    )

    def get_pricelist_version_domain(self):
        return [('pricelist_id.price_grid', '=', True)]

    def get_default_pricelist_item_vals(self, version):
        return {
            'price_version_id': version.id,
            'price_discount': -1,
            'base': 1,
        }

    def default_pricelist_item_ids(self):
        versions = self.env['product.pricelist.version'].search(
            self.get_pricelist_version_domain())
        res = []
        for version in versions:
            res.append(self.get_default_pricelist_item_vals(version))
        return res

    @api.model
    def create(self, vals):
        if 'pricelist_item_ids' in vals:
            self.create_or_write_pricelist(vals['pricelist_item_ids'])
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'pricelist_item_ids' in vals:
            self.create_or_write_pricelist(vals['pricelist_item_ids'])
        return super(ProductTemplate, self).write(vals)

    @api.model
    def create_or_write_pricelist(self, pricelist_item_vals):
        for version in pricelist_item_vals:
            if version[2]:
                self.update_pricelist_values(version[2])
        return True

    @api.model
    def update_pricelist_values(self, vals):
        vals.update({
            'price_discount': -1,
            'sequence': 1,
            'base': 1,
        })
        return True
