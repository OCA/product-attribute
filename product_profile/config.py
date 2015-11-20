# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models
from .product import PROFILE_MENU


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    group_product_profile = fields.Boolean(
        string="Display Product Profile fields",
        implied_group='product_profile.group_product_profile',
        help="Display fields computed by product profile "
             "module.\nFor debugging purpose see menu\n%s" % PROFILE_MENU)
