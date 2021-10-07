# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    weekly_sold_delivered_shown = fields.Char(
        string="Weekly Sold", related="product_id.weekly_sold_delivered_shown",
    )
