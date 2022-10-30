# Copyright 2023 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def rename_type_to_detailed_type(env):
    if openupgrade.column_exists(env.cr, "product_profile", "type"):
        openupgrade.rename_columns(
            env.cr,
            {
                "product_profile": [
                    ("type", "detailed_type"),
                ],
            },
        )


@openupgrade.migrate()
def migrate(env, version):
    rename_type_to_detailed_type(env)
