# -*- coding: utf-8 -*-
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2015 Camptocamp SA                                              #
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from openerp import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    supplier_code = fields.Char('Supplier Product Code', readonly=True,
                                compute='_get_supplier_code',
                                search='_search_supplier_code')

    @api.depends('seller_ids.product_code')
    def _get_supplier_code(self):
        for product in self:
            if product.seller_ids:
                product.supplier_code = product.seller_ids[0].product_code
            else:
                product.supplier_code = ''

    def _search_supplier_code(self, operator, value):
        supplierinfos = self.env['product.supplierinfo'].search(
            [('product_code', operator, value)]
        )

        product_ids = (
            supplierinfos
            and supplierinfos.mapped('product_tmpl_id.product_variant_ids').ids
            or []
        )
        return [('id', 'in', product_ids)]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Try to find complete matches on supplier code. Otherwise, super().

        """
        if args is None:
            args = []

        found_by_supplier_code = self.search(
            [('supplier_code', '=ilike', name)] + args, limit=limit
        )
        if found_by_supplier_code:
            return found_by_supplier_code.name_get()
        else:
            return super(Product, self).name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit)
