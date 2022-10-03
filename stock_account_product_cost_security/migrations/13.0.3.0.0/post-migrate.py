# Copyright 2022 Tecnativa - David Vidal
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # By default we're granting all the users the same permission the had prior to
    # this version change. Is up to every admin to manage proper permissions.
    env.ref(
        "stock_account_product_cost_security.group_product_edit_cost"
    ).users = env.ref("product_cost_security.group_product_cost").users
