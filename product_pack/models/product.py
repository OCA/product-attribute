# -*- coding: utf-8 -*-
# Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#                     All Rights Reserved.
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.exceptions import Warning
import math


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pack_line_ids = fields.One2many(
        'product.pack.line',
        'parent_product_id',
        'Pack Products',
        help='List of products that are part of this pack.')
    used_pack_line_ids = fields.One2many(
        'product.pack.line',
        'product_id',
        'On Packs',
        help='List of packs where product is used.')

    @api.multi
    def _product_available(self, field_names=None, arg=False):
        """For product packs we get availability in a different way."""
        result = (super(ProductProduct, self.filtered("pack"))
                  ._product_available(field_names, arg))

        for product in self.filtered(lambda record: not record.pack):
            pack_qty_available = []
            pack_virtual_available = []
            for subproduct in product.pack_line_ids:
                subproduct_stock = subproduct.product_id._product_available(
                    field_names, arg)[subproduct.product_id.id]
                sub_qty = subproduct.quantity
                if sub_qty:
                    pack_qty_available.append(math.floor(
                        subproduct_stock['qty_available'] / sub_qty))
                    pack_virtual_available.append(math.floor(
                        subproduct_stock['virtual_available'] / sub_qty))

            # TODO Calculate correctly pack virtual available for negatives
            result[product.id] = {
                'qty_available': (
                    pack_qty_available and min(pack_qty_available) or False),
                'incoming_qty': 0,
                'outgoing_qty': 0,
                'virtual_available': (
                    pack_virtual_available and
                    max(min(pack_virtual_available), 0) or False),
            }
        return result

    @api.multi
    @api.constrains('pack_line_ids')
    def check_recursion(self):
        """Check recursion on packs."""
        pack_lines = self.mapped("pack_line_ids")
        while pack_lines:
            if self in pack_lines.mapped('product_id'):
                raise Warning(_(
                    'Error! You cannot create recursive packs.\n'
                    'Product id: %s') % self.id)
            pack_lines = pack_lines.mapped('product_id.pack_line_ids')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pack_type = fields.Selection(
        [('components_price', 'Detailed Component Prices'),
         ('totalize_price', 'Detailed Totalized Price'),
         ('fixed_price', 'Detailed Fixed Price'),
         ('none_detailed_totalized_price', 'Not Detailed Totalized Price'),
         ('none_detailed_assited_price', 'Not Detailed Assisted Price')],
        'Pack Type',
        oldname="pack_price_type",
        help="* Detailed Components Prices: This product and its subproducts "
             "cost their chosen price.\n"
             "* Detailed Totalized Price: This product costs the sum of its "
             "subproducts prices. Subproducts cost zero. This product's price "
             "is ignored.\n"
             "* Detailed Fixed Price: This product costs its price. "
             "Subproducts cost zero.\n"
             "* Not Detailed Totalized Price: Like 'Detailed Totalized "
             "Price', but subproducts are not shown.\n"
             "* Not Detailed Assisted Price: Like 'Not Detailed Totalized "
             "Price', but with a button to edit the details.")
    pack = fields.Boolean(
        'Pack',
        help='Is a Product Pack?')
    pack_line_ids = fields.One2many(
        related='product_variant_ids.pack_line_ids')
    used_pack_line_ids = fields.One2many(
        related='product_variant_ids.used_pack_line_ids')

    @api.multi
    @api.constrains('pack_line_ids', 'pack_type', 'pack')
    def check_relations(self):
        """Check assited packs do not have packs as childs."""
        for s in self.filtered(lambda record: (record.pack_type ==
                                               'none_detailed_assited_price')):
            if s.mapped('pack_line_ids.product_id').filtered('pack'):
                raise Warning(_(
                    'A "Not Detailed Assisted Price" pack cannot have a '
                    'pack as a child!'))

    @api.multi
    @api.constrains('company_id', 'pack_line_ids', 'used_pack_line_ids')
    def check_pack_line_company(self):
        """Check that packs are related to packs of same company."""
        for s in self:
            for line in s.pack_line_ids:
                if line.product_id.company_id != s.company_id:
                    raise Warning(_(
                        "Pack line product's company must be the same as the "
                        "parent product's."))
            for line in s.used_pack_line_ids:
                if line.parent_product_id.company_id != s.company_id:
                    raise Warning(_(
                        "Pack line product's company must be the same as the "
                        "parent product's."))

    @api.multi
    def write(self, vals):
        """We remove from ``product.product`` to avoid error."""
        if vals.get('pack_line_ids', False):
            self.product_variant_ids.write(
                {'pack_line_ids': vals.pop('pack_line_ids')})
        return super(ProductTemplate, self).write(vals)

    @api.model
    def _price_get(self, products, ptype='list_price'):
        """Modify price of product if pack is configured to do so."""
        res = super(ProductTemplate, self)._price_get(
            products, ptype=ptype)
        price_modifier_types = {
            'totalize_price',
            'none_detailed_assited_price',
            'none_detailed_totalized_price',
        }
        for product in products:
            if product.pack and product.pack_type in price_modifier_types:
                pack_price = 0.0
                for pack_line in product.pack_line_ids:
                    product_line_price = pack_line.product_id.price_get()[
                        pack_line.product_id.id]
                    pack_price += (product_line_price * pack_line.quantity)
                res[product.id] = pack_price
        return res
