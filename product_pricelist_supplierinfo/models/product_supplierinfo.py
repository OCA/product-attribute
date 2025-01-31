# Copyright 2020 Akretion - Mourad EL HADJ MIMOUNE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    sale_margin = fields.Float(
        default=0,
        digits=(16, 2),
        string="Sale Margin (%)",
        help="Margin to apply on price to obtain sale price",
    )

    def _get_supplierinfo_pricelist_price(self, no_supplierinfo_discount=False):
        self.ensure_one()
        sale_price = self.price if no_supplierinfo_discount else self.price_discounted
        if self.sale_margin:
            sale_price = (sale_price + (sale_price * (self.sale_margin / 100))) or 0.0
        return sale_price
