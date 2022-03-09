# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    if column_exists(cr, "product_supplierinfo", "supplierinfo_group_id"):
        rename_column(cr, "product_supplierinfo", "supplierinfo_group_id", "group_id")
