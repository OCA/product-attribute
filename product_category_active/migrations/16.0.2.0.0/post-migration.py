# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    action = env.ref("product.product_category_action_form")
    current_context = safe_eval(action.context)
    if "active_test" in current_context:
        _logger.info("Removing active_test on product_category_action_form")
        del current_context["active_test"]
        action.context = current_context
