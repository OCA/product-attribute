# -*- coding: utf-8 -*-
# © 2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, exceptions, fields, models
from openerp.tools.translate import _


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.multi
    @api.depends('product_id', 'product_tmpl_id', 'categ_id')
    def _compute_fallback(self):
        for rec in self:
            if not rec.product_id and not rec.product_tmpl_id \
                and not rec.categ_id:
                    rec.fallback = True

    fallback = fields.Boolean(
        string='Fallback',
        help='True if it matches all the products',
        compute='_compute_fallback',
        store=True)

    @api.one
    @api.constrains('product_tmpl_id', 'categ_id', 'base_pricelist_id')
    def _check_pricelist_item_fields(self):
        if self.product_tmpl_id and self.categ_id:
            raise exceptions.ValidationError(
                _('Cannot use both Product Template and Product Category'))
        elif not self.product_tmpl_id and not self.categ_id \
            and not self.base_pricelist_id:
                raise exceptions.ValidationError(
                    _('One of Product Template, Product Category '
                        'or Other Pricelist must be filled'))
