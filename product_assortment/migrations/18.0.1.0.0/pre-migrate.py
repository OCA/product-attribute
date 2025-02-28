# Copyright (C) 2025 The O-team <https://www.the-o-team.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, version):
    """Update the `domain` value to `[(1, "=", 0)]`.

    This is needed to retain the behavior of the module available in older versions of
    the module. In older versions, the `whitelist_product_ids` field was not required
    to be set explicitly to a void domain when used in combination with the
    'whitelisted_product_ids' field. When the `whitelist_product_ids` field was empty,
    the `domain` field was ignored.

    However, due to a change in the ORM, the `domain` field is now always applied,
    even if the `whitelist_product_ids` field is empty. This change has caused the
    behavior to differ from previous versions of the module.

    To restore the previous behavior, we need to set the `domain` field to a
    non-empty domain, such as `[(1, "=", 0)]`, which will always return False and
    effectively ignore the `domain` field.
    """
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_filters irf
        SET domain = '[("id", "=", 0)]'
        WHERE irf.is_assortment = True
        AND irf.domain = '[]'
        AND EXISTS(
            SELECT 1
            FROM assortment_product_whitelisted apw
            WHERE apw.ir_filters_id = irf.id
        )
        """,
    )
