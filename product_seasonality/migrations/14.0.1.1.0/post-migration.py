# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Set product_template_id on seasonal config lines")
    config_lines = env["seasonal.config.line"].search(
        [("product_template_id", "=", False)]
    )
    for config_line in config_lines:
        config_line.product_template_id = config_line.product_id.product_tmpl_id
