# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

_xmlid_renames = [
    # rename suffix:
    (
        "product_expiry_configurable.ir_cron_product_expiry_life_date",
        "product_expiry_configurable.ir_cron_product_expiry_expiration_date",
    ),
]
_column_renames = {
    "product_category": [
        ("specific_life_time", "specific_expiration_time"),
    ],
    "product_template": [
        ("specific_life_time", "specific_expiration_time"),
    ],
    "stock_production_lot": [
        ("life_date_reminded", "expiration_date_reminded"),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, _xmlid_renames)
    openupgrade.rename_columns(env.cr, _column_renames)
    openupgrade.logged_query(
        env.cr,
        """
    UPDATE product_category
    SET specific_compute_dates_from = 'expiration_date'
    WHERE specific_compute_dates_from = 'life_date'
    """,
    )
    openupgrade.logged_query(
        env.cr,
        """
    UPDATE product_template
    SET specific_compute_dates_from = 'expiration_date'
    WHERE specific_compute_dates_from = 'life_date'
    """,
    )
