# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.product_state.hooks import post_init_hook


def migrate(cr, version):
    post_init_hook(cr, False)
