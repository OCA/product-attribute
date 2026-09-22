# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    group = env.ref("stock_lot_unique_name.group_allow_duplicate_lot_name")
    internal_users = (
        env["res.users"].with_context(active_test=False).search([("share", "=", False)])
    )
    # remove default user template to avoid assigning new users to the group
    internal_users -= (
        env.ref("base.default_user", raise_if_not_found=False) or env["res.users"]
    )
    group.sudo().users |= internal_users
    _logger.info(
        "Allowed %s existing internal users to add duplicate lot names",
        len(internal_users),
    )
