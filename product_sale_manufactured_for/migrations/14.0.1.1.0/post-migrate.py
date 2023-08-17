# Copyright 2023 Camptocamp SA (http://www.camptocamp.com)
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api, tools

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    bkp_table = "product_template_res_partner_rel_bkp"
    if not tools.sql.table_exists(cr, bkp_table):
        return

    # Use backup table (created by pre-migrate step)
    api.Environment(cr, SUPERUSER_ID, {})
    query = """
        INSERT INTO product_product_manuf_for_partner_rel
        SELECT * FROM product_template_res_partner_rel_bkp
    """
    cr.execute(query)
    cr.execute("DROP TABLE product_template_res_partner_rel_bkp")
    _logger.info("Table migrated")
