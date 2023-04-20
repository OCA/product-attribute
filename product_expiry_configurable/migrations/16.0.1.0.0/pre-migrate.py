# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _create_columns(env):
    """
    Create columns to fill in the previous module 'specific' fields
    """
    field_names = [
        (
            "expiration_time",
            "product.category",
            "product_category",
            "integer",
            "integer",
            "product_expiry_configurable",
        ),
        (
            "use_time",
            "product.category",
            "product_category",
            "integer",
            "integer",
            "product_expiry_configurable",
        ),
        (
            "removal_time",
            "product.category",
            "product_category",
            "integer",
            "integer",
            "product_expiry_configurable",
        ),
        (
            "alert_time",
            "product.category",
            "product_category",
            "integer",
            "integer",
            "product_expiry_configurable",
        ),
    ]
    if not openupgrade.column_exists(env.cr, "product_category", "expiration_time"):
        openupgrade.add_fields(env, field_names)


@openupgrade.migrate()
def migrate(env, version):
    _create_columns(env)
