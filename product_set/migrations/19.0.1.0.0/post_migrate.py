# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "product.set.line",
                env["product.set.line"]._table,
                "product_packaging_id",
                "product_uom_id",
            ),
        ],
    )
