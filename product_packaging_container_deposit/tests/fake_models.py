# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ContainerDepositOrderTest(models.Model):
    _name = "container.deposit.order.test"
    _inherit = ["container.deposit.order.mixin"]
    _description = "Model used only for test"

    name = fields.Char()
    partner_id = fields.Many2one("res.partner")
    company_id = fields.Many2one("res.company")
    state = fields.Char()
    order_line = fields.One2many(
        "container.deposit.order.line.test", inverse_name="order_id"
    )

    def _get_order_line_field(self):
        return "order_line"


class ContainerDepositOrderLineTest(models.Model):
    _name = "container.deposit.order.line.test"
    _inherit = ["container.deposit.order.line.mixin"]
    _description = "Model used only for test"

    name = fields.Char()
    order_id = fields.Many2one("container.deposit.order.test")
    product_id = fields.Many2one("product.product")
    product_qty = fields.Float()
    product_packaging_id = fields.Many2one("product.packaging")
    qty_delivered = fields.Float()
    sequence = fields.Integer(default=10)

    def _get_product_qty_field(self):
        return "product_qty"

    def _get_product_qty_delivered_received_field(self):
        return "qty_delivered"
