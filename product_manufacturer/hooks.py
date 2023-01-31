# Copyright 2022 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tools import sql


def pre_init_hook(cr):
    table_name = "product_template"
    for field_name, field_type in [
        ("manufacturer", "int4"),
        ("manufacturer_pname", "varchar"),
        ("manufacturer_pref", "varchar"),
        ("manufacturer_purl", "varchar"),
    ]:
        if sql.column_exists(cr, table_name, field_name):
            continue
        sql.create_column(cr, table_name, field_name, field_type)
