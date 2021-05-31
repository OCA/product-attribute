# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tools.sql import rename_column


def migrate(cr, version):
    # Rename packaging_length into lnght (keeping name consistency across modules)
    rename_column(cr, "product_packaging", "packaging_length", "lnght")
