# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr,
        "product_pricelist_direct_print",
        "migrations/15.0.1.1.1/noupdate_changes.xml",
    )
    openupgrade.delete_record_translations(
        env.cr,
        "product_pricelist_direct_print",
        ["email_template_edi_pricelist"],
    )
