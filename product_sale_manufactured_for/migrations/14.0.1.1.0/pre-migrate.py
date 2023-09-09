# Copyright 2023 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import tools

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    # Backup old relation to be used later on post migrate
    old_table = "product_template_res_partner_rel"
    if not tools.sql.table_exists(cr, old_table):
        return
    bkp_table = "product_template_res_partner_rel_bkp"
    if tools.sql.table_exists(cr, bkp_table):
        return

    bkp_query = """
    CREATE TABLE IF NOT EXISTS
        product_template_res_partner_rel_bkp
    AS
        SELECT
            prod.id as product_id,
            rel.res_partner_id as partner_id
        FROM
            product_product prod,
            product_template_res_partner_rel rel
        WHERE
            prod.product_tmpl_id = rel.product_template_id;
    """
    cr.execute(bkp_query)
    _logger.info("Relations backed up")

    # cleanup  possibly broken views
    cr.execute(
        """
        DELETE FROM ir_ui_view
        WHERE model = 'product.template'
        AND arch_db like '%manufactured_for_partner_ids%';
    """
    )
    _logger.info("Views cleaned up")
