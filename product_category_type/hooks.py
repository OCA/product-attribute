# Copyright 2021 Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _logger.info("Initialize view categories ...")
    cr.execute(
        """
        UPDATE product_category
            SET type = 'view'
            WHERE id in (
                SELECT parent_id
                FROM product_category)
            AND id not in (
                SELECT categ_id
                FROM product_template);
        """
    )
