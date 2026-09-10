# Copyright 2025 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, "product_packaging_level", "migrations/16.0.1.0.0/noupdate_changes.xml"
    )
    openupgrade.delete_record_translations(
        env.cr,
        "product_packaging_level",
        ["product_packaging_level_default"],
        ["name"],
    )
