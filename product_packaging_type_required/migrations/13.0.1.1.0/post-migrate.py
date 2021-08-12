# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("product_packaging_type_required: fix 'Packaging Required' cron")
    # This cron has `noupdate` on, we must fix it here
    cron = env.ref("product_packaging_type_required.ir_cron_packaging_required", False)
    if cron:
        cron.code = "model.cron_check_create_required_packaging()"
