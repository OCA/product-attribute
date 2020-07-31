# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    group_id = env.ref('product_multi_price.group_show_multi_prices').id
    default_user = env.ref('base.default_user')
    user = env['res.users'].with_context(active_test=False).search(
        [("share", "=", False)])
    (user - default_user).write({'groups_id': [(4, group_id, None)]})
