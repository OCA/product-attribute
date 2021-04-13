# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def _move_history_state_field(env):
    field_spec = [
        (
            "product_state_id",
            "product.state.history",
            "product_state_history",
            "many2one",
            "integer",
            "product_state_history",
        )
    ]
    openupgrade.add_fields(env, field_spec)
    query = """
        UPDATE product_state_history psh
            SET product_state_id =
            (SELECT id FROM product_state WHERE code = psh.product_state)
    """
    env.cr.execute(query)


@openupgrade.migrate()
def migrate(env, version):
    _move_history_state_field(env)
