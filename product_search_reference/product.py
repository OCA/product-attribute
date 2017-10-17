##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api


class Product(models.Model):
    _inherit = 'product.product'

    def _search_partner_ref2(self, operator, value):
        suppliferinfo_obj = self.env['product.supplierinfo']

        domain = [('product_code', operator, value)]
        supplierinfo_ids = suppliferinfo_obj.search(domain)

        product_ids = []

        for vendor in supplierinfo_ids:
            if vendor.product_id:
                product_ids.append(vendor.product_id.id)
            elif vendor.product_tmpl_id:
                product_ids += vendor.product_tmpl_id.product_variant_ids.ids

        return [('id', 'in', product_ids)]

    partner_ref2 = fields.Char(
        compute="_compute_partner_ref2",
        search="_search_partner_ref2",
        string="Supplier ref",
    )

    @api.multi
    @api.depends(
        'seller_ids',
        'seller_ids.product_code',
    )
    def _compute_partner_ref2(self):
        for product in self:
            refs = [
                supplier.product_code
                for supplier in product.seller_ids
                if supplier.product_code
            ]
            product.partner_ref2 = "\n".join(refs)

    @api.model
    def name_search(
        self,
        name='',
        args=None,
        operator='ilike',
        limit=100
    ):
        domain = [('partner_ref2', operator, name)] + args
        result = self.search(domain, limit=limit)

        if result:
            return result.name_get()

        return super(Product, self).name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit
        )
