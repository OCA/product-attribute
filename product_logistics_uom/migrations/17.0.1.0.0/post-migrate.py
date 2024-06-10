# Copyright 2023 ACSONE SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import SUPERUSER_ID, api

# pylint: disable=odoo-addons-relative-import
from odoo.addons.product_logistics_uom.hooks import pre_init_hook


def migrate(cr, version):
    """Migrate data from product_logistics_uom module."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    pre_init_hook(env)
