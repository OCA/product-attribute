# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):

    # Rename lngth into packaging_length
    if column_exists(cr, "product_packaging", "packaging_length"):
        cr.execute("UPDATE product_packaging SET packaging_length = lngth")
    elif column_exists(cr, "product_packaging", "lngth"):
        rename_column(cr, "product_packaging", "lngth", "packaging_length")
