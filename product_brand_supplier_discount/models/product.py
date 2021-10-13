# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    fixed_discount = fields.Float(string="Fixed Discount", readonly=True)
    set_fixed_discount = fields.Boolean(string="Set fixed discount")
    discount = fields.Float(string='Discount', compute="_compute_discount",
                            inverse="_set_discount", store=True)

    @api.depends(
        'name',
        'product_tmpl_id.product_brand_id.supplier_discount_ids',
        'product_tmpl_id.product_brand_id.supplier_discount_ids.partner_id',
        'product_tmpl_id.product_brand_id.supplier_discount_ids.discount',
        'product_id.product_brand_id.supplier_discount_ids',
        'product_id.product_brand_id.supplier_discount_ids.partner_id',
        'product_id.product_brand_id.supplier_discount_ids.discount',)
    def _compute_discount(self):
        # computes the discount suggested by supplier and brand.
        for supplierinfo in self:
            brand = False
            if supplierinfo.set_fixed_discount:
                supplierinfo.discount = supplierinfo.fixed_discount
            else:
                if supplierinfo.product_tmpl_id:
                    brand = supplierinfo.product_tmpl_id.product_brand_id
                elif supplierinfo.product_id:
                    brand = supplierinfo.product_id.product_brand_id
                if brand:
                    for supplier_discount in brand.supplier_discount_ids:
                        if supplier_discount.partner_id == supplierinfo.name:
                            supplierinfo.discount = supplier_discount.discount

    @api.multi
    def _set_discount(self):
        # user can edit discount of a supplierinfo:
        self.ensure_one()
        self.fixed_discount = self.discount
        self.set_fixed_discount = True
