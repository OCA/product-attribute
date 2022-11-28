# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Initialize expiry_date on table stock_production_lot")
    cr.execute(
        """
        ALTER TABLE stock_lot
            ADD COLUMN IF NOT EXISTS expiry_date timestamp without time zone;
        CREATE INDEX IF NOT EXISTS"stock_lot_expiry_date_index"
            ON "stock_lot" ("expiry_date");
    """
    )
    cr.execute(
        """
        UPDATE stock_lot
        SET expiry_date = removal_date;
    """
    )
