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
        _rename_field_record(cr)
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


def _rename_field_record(cr):
    """Rename the field record and its xmlid, or Odoo drops the old field."""
    cr.execute(
        """
        UPDATE ir_model_fields
           SET name = 'uom_id'
         WHERE model = 'product.customerinfo'
           AND name = 'product_uom_id'
           AND NOT EXISTS (SELECT 1 FROM ir_model_fields
                            WHERE model = 'product.customerinfo' AND name = 'uom_id')
        """
    )
    cr.execute(
        """
        UPDATE ir_model_data
           SET name = 'field_product_customerinfo__uom_id'
         WHERE module = 'product_customerinfo'
           AND model = 'ir.model.fields'
           AND name = 'field_product_customerinfo__product_uom_id'
           AND NOT EXISTS (SELECT 1 FROM ir_model_data
                            WHERE module = 'product_customerinfo'
                              AND name = 'field_product_customerinfo__uom_id')
        """
    )
