# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

_logger = logging.getLogger(__name__)


def column_exists(cr, tablename, columnname):
    """ Return whether the given column exists. """
    query = """ SELECT 1 FROM information_schema.columns
                WHERE table_name=%s AND column_name=%s """
    cr.execute(query, (tablename, columnname))
    return cr.rowcount


def pre_init_hook(cr):
    _logger.info("Initialize expiry_date on table stock_production_lot")
    if not column_exists(cr, "stock_production_lot", "expiry_date"):
        cr.execute(
            """
            ALTER TABLE stock_production_lot
                ADD COLUMN expiry_date timestamp without time zone;
            CREATE INDEX "stock_production_lot_expiry_date_index"
                ON "stock_production_lot" ("expiry_date");
        """
        )
    cr.execute(
        """
        UPDATE stock_production_lot
        SET expiry_date = removal_date;
    """
    )
