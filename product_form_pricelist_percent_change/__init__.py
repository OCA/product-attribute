#  Copyright 2023 Francesco Ballerini
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from . import models
from odoo import api, SUPERUSER_ID


def _post_init_hook(cr, registry):
    """Enable user input div visibility on pre-existent pricelist rules"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute(
        """UPDATE product_pricelist_item SET show_percent_change_button = true;"""
    )
