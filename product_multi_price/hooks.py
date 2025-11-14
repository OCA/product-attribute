# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command


def post_init_hook(env):
    group = env.ref("product_multi_price.group_show_multi_prices")
    # New internal users get the implied groups of the default user group
    default_user_group = env.ref("base.default_user_group", raise_if_not_found=False)
    if default_user_group:
        default_user_group.write({"implied_ids": [Command.link(group.id)]})
    users = (
        env["res.users"].with_context(active_test=False).search([("share", "=", False)])
    )
    users.write({"group_ids": [Command.link(group.id)]})
