# Copyright 2023 Camptocamp SA (http://www.camptocamp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    api.Environment(cr, SUPERUSER_ID, {})
    query = """
        DELETE FROM product_product_manuf_for_partner_rel
            WHERE partner_id IN (
                SELECT id FROM res_partner WHERE active = false
            );
    """
    cr.execute(query)
    _logger.info("Cleanup archived users from Manufactured For field.")
