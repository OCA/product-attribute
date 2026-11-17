# Copyright 2026 INVITU
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    margin = fields.Monetary(groups="product_cost_security.group_product_cost")
    margin_percent = fields.Float(groups="product_cost_security.group_product_cost")
