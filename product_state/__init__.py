# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models


def post_init_hook(env):
    """This hook is used to add a state on existing products
    when module product_state is installed.
    """

    product_without_state = env["product.template"].search([("state", "=", False)])
    product_without_state.write({"state": "sellable"})
    product_without_state = env["product.template"].search(
        [("product_state_id", "=", False)]
    )
    product_without_state._inverse_product_state()
