# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_no_list_price = fields.Boolean(
        "Hide field 'Sales price'",
        help=("Use fixed price and hide the native 'Sales Price' field"),
        implied_group="product_form_pricelist.group_no_list_price",
    )
