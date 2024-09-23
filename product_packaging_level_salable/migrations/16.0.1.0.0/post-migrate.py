# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def _fill_in_columns(env):
    if openupgrade.column_exists(env.cr, "product_packaging", "can_be_sold"):
        query = """
            UPDATE product_packaging
            SET sales = can_be_sold
        """
        openupgrade.logged_query(env.cr, query)


@openupgrade.migrate()
def migrate(env, version):
    _fill_in_columns(env)
