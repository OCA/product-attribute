# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade
from psycopg2.extensions import AsIs

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    logger.info(
        "Create product.print.category.rule based on "
        "print_category_id on res.company field ..."
    )
    old_column = AsIs(openupgrade.get_legacy_name("print_category_id"))
    env.cr.execute(
        """
        SELECT id, %s
        FROM res_company
        WHERE %s is not null;
        """,
        (old_column, old_column),
    )
    i = 0
    for row in env.cr.fetchall():
        i += 1
        vals = {
            "sequence": i,
            "main_category_id": False,
            "print_category_id": row[1],
            "company_id": row[0],
        }
        env["product.print.category.rule"].create(vals)
