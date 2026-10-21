# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from odoo.tools import sql

_logger = logging.getLogger(__name__)

TABLE = "product_customerinfo"


def migrate(cr, version):
    """Keep the customer specific unit of measure.

    In 20.0 ``product.supplierinfo.product_uom_id`` is renamed to ``uom_id``.
    ``product.customerinfo`` copies that field into its own table, so the column
    has to follow, otherwise ``uom_id`` is recomputed from the product and the
    unit of measure set for the customer is lost.
    """
    if not sql.column_exists(cr, TABLE, "product_uom_id"):
        return
    if not sql.column_exists(cr, TABLE, "uom_id"):
        _logger.info("Renaming %s.product_uom_id to uom_id", TABLE)
        sql.rename_column(cr, TABLE, "product_uom_id", "uom_id")
        return
    _logger.info("Copying %s.product_uom_id to uom_id", TABLE)
    cr.execute(
        """
        UPDATE product_customerinfo
           SET uom_id = product_uom_id
         WHERE product_uom_id IS NOT NULL
           AND uom_id IS DISTINCT FROM product_uom_id
        """
    )
