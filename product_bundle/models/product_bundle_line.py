# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import _, api, fields, models


class ProductBundleLine(models.Model):
    _name = "product.bundle.line"
    _rec_name = "bundle_id"
    _sql_constraints = [
        ('bundle_product', 'unique(bundle_id, product_id)',
         _("You cannot bundle the same product several times.")),
    ]

    bundle_id = fields.Many2one(
        "product.product",
        "Bundle",
        domain=[("bundle_ok", "=", True)],
        ondelete="cascade",
        required=True,
    )
    qty = fields.Float(
        "Quantity",
        required=True,
        default=1,
    )
    product_id = fields.Many2one(
        "product.product",
        "Product",
        ondelete="cascade",
        required=True,
    )
    currency_id = fields.Many2one(related="product_id.currency_id")
    total_lst_price = fields.Monetary(
        string="Total Public Price",
        currency_field="currency_id",
        compute="_compute_total_lst_price",
        help="Total price of bundled products.",
    )

    @api.one
    @api.depends("product_id.lst_price", "qty")
    def _compute_total_lst_price(self):
        self.total_lst_price = self.qty * self.product_id.lst_price
