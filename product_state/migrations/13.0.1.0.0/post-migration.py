# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936

from odoo.addons.product_state import post_init_hook


@openupgrade.migrate()
def migrate(env, version):
    post_init_hook(env.cr, env)
