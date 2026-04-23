# Copyright 2026 ForgeFlow
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE abc_classification_product_level AS lvl
        SET company_id = tmpl.company_id
        FROM product_product AS pp,
             product_template AS tmpl
        WHERE lvl.product_id = pp.id
          AND pp.product_tmpl_id = tmpl.id
          AND tmpl.company_id IS NOT NULL
          AND lvl.company_id IS NULL;
        """
    )
    _logger.info(
        "Backfilled company_id on %s abc.classification.product.level rows",
        cr.rowcount,
    )
