# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSetLine(models.Model):
    _name = "product.set.line"
    _description = "Product set line"
    _rec_name = "product_id"
    _order = "product_set_id, sequence, product_id"

    product_id = fields.Many2one(
        comodel_name="product.product",
        domain=[("sale_ok", "=", True)],
        string="Product",
        required=True,
    )
    quantity = fields.Float(
        digits="Product Unit of Measure", required=True, default=1.0
    )
    product_set_id = fields.Many2one("product.set", string="Set", ondelete="cascade")
    active = fields.Boolean(
        string="Active", related="product_set_id.active", store=True, readonly=True
    )
    sequence = fields.Integer(required=True, default=0)
    company_id = fields.Many2one(
        "res.company", related="product_set_id.company_id", store=True, readonly=True
    )
