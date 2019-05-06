# -*- coding: utf-8 -*-
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = "sale.config.settings"

    stock_state_threshold = fields.Float(
        related="company_id.stock_state_threshold",
        string="Stock State Threshold *",
        help="Define custom value"
        " under wich the stock state will pass from 'In Stock' to 'In Limited"
        " Stock' State.",
    )
