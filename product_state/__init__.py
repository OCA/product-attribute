# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models
from odoo.orm.domains import Domain


def post_init_hook(env):
    """Add a state on existing products"""
    tmpl_obj = env["product.template"].with_context(active_test=False)
    tmpl_without_state = tmpl_obj.search(Domain("state", "=", False))
    tmpl_without_state.write({"state": "sellable"})
    tmpl_without_state_id = tmpl_obj.search(Domain("product_state_id", "=", False))
    tmpl_without_state_id._inverse_product_state()
