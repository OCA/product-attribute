# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """ This hook is used to add a state on existing products
    when module product_state is installed.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    product_without_state = env["product.template"].with_context(
        active_test=False,
    ).search(
        [("product_state_id", "=", False), ("state", "!=", False)]
    )
    product_without_state._inverse_product_state()
