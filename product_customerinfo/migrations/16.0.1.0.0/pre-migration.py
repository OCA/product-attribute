from openupgradelib import openupgrade

column_renames = {
    "product_customerinfo": [("name", "partner_id")],
}


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "product_customerinfo", "name"):
        openupgrade.rename_columns(env.cr, column_renames)
