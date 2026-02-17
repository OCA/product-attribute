# Copyright 2026 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        "UPDATE product_pricelist_item SET no_supplierinfo_discount=True",
    )
    env["ir.default"].set("product.pricelist.item", "no_supplierinfo_discount", "true")
