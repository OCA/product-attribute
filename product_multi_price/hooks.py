# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    group_id = env.ref("product_multi_price.group_show_multi_prices").id
    user = (
        env["res.users"].with_context(active_test=False).search([("share", "=", False)])
    )
    # In Odoo 19, there isn't a specific base.default_user,
    # so apply to all non-portal users
    user.write({"group_ids": [(4, group_id, None)]})
