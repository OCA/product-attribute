# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from .product_profile import PROFILE_MENU


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_product_profile = fields.Boolean(
        string="Display Product Profile fields",
        implied_group="product_profile.group_product_profile_user",
        help="Display fields computed by product profile "
        "module.\nFor debugging purpose see menu\n%s" % PROFILE_MENU,
    )
