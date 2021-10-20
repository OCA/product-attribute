# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from . import models


from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """This hook is used to add a state on existing products
    when module product_state is installed.
    """
    query = """
        UPDATE product_template
            SET product_state_id = data.product_state_id
            FROM
            (SELECT tmpl.id as tmpl_id, product_state_id
            FROM product_template tmpl
            JOIN product_state ps on ps.code = tmpl.state) AS data
            WHERE product_template.id = data.tmpl_id
    """
    cr.execute(query)
