#  Copyright 2020 Tecnativa - Ernesto Tejeda
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
from odoo.addons.product_multi_price.hooks import post_init_hook


def migrate(cr, version):
    post_init_hook(cr, False)
