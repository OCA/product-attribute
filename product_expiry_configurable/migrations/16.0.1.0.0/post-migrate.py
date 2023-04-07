# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


def _fill_in_columns(env):
    """
    Create columns to fill in the previous module 'specific' fields
    """
    if openupgrade.column_exists(
        env.cr, "product_category", "specific_expiration_time"
    ):
        query = """
            UPDATE product_category
                SET expiration_time = specific_expiration_time
        """
        openupgrade.logged_query(env.cr, query)
    if openupgrade.column_exists(env.cr, "product_category", "specific_use_time"):
        query = """
            UPDATE product_category
                SET use_time = specific_use_time
        """
        openupgrade.logged_query(env.cr, query)
    if openupgrade.column_exists(env.cr, "product_category", "specific_use_time"):
        query = """
            UPDATE product_category
                SET use_time = specific_use_time
        """
        openupgrade.logged_query(env.cr, query)
    if openupgrade.column_exists(env.cr, "product_category", "specific_removal_time"):
        query = """
            UPDATE product_category
                SET removal_time = specific_removal_time
        """
        openupgrade.logged_query(env.cr, query)
    if openupgrade.column_exists(env.cr, "product_category", "specific_alert_time"):
        query = """
            UPDATE product_category
                SET alert_time = specific_alert_time
        """
        openupgrade.logged_query(env.cr, query)


@openupgrade.migrate()
def migrate(env, version):
    _fill_in_columns(env)
