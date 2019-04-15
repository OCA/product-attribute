#  Copyright 2019 Tecnativa - Sergio Teruel
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    group_secondary_unit = env.ref(
        'product_secondary_unit.group_secondary_unit')
    users = env['res.users'].with_context(active_test=False).search([])
    users.write({
        'groups_id': [(4, group_secondary_unit.id)]
    })
