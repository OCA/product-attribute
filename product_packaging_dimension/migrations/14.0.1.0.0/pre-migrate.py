# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    # Rename lnght into packaging_length
    if column_exists(cr, "product_packaging", "lnght"):
        rename_column(cr, "product_packaging", "lnght", "packaging_length")

        # Convert old hard-coded uom values (mm)
        # into new default uom values (m)
        cr.execute(
            """
        UPDATE product_packaging
        SET
        packaging_length = packaging_length/1000,
        height = height/1000,
        width = width/1000,
        """
        )
