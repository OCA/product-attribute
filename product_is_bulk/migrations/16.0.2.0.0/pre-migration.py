# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("[product_is_bulk] Add column `is_bulk`.")
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE product_product
        ADD COLUMN IF NOT EXISTS is_bulk boolean
    """,
    )

    _logger.info("[product_is_bulk] Pre-filled computed field `is_bulk`.")
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE product_product pp
        SET is_bulk = (
            uc.measure_type IN ('weight', 'volume')
        )
        FROM product_template pt
        JOIN uom_uom uom
         ON uom.id = pt.uom_id
        JOIN uom_category uc
         ON uc.id = uom.category_id
        WHERE pp.product_tmpl_id = pt.id;
    """,
    )
