# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


column_renames = {
    "res_company": [
        ("print_category_id", None),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    logger.info("Preserve default print_category_id on res.company field ...")
    openupgrade.rename_columns(env.cr, column_renames)
