# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_state_threshold = fields.Float(
        related="company_id.stock_state_threshold",
        string="Stock State Threshold",
        readonly=False,
        help="Define custom value"
        " under which the stock state will pass from 'In Stock' to 'In Limited"
        " Stock' State.",
    )
