# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _move_max_weight(env):
    """
    Move max_weight value to weight if not defined
    """
    if openupgrade.column_exists(env.cr, "product_packaging", "max_weight"):
        query = """
            UPDATE product_packaging
                SET weight = max_weight
                WHERE weight IS NULL OR weight = 0.0
                AND max_weight IS NOT NULL
                AND product_id IS NOT NULL
        """
        openupgrade.logged_query(env.cr, query)


@openupgrade.migrate()
def migrate(env, version):
    _move_max_weight(env)
