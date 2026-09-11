# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools import split_every


def post_init_hook(env):
    """Backfill packagings for products that already have ``uom_ids`` set.

    Processed in batches so the ORM cache does not grow unbounded on large
    catalogs.
    """
    products = env["product.product"].search([("uom_ids", "!=", False)])
    for batch_ids in split_every(1000, products.ids):
        env["product.product"].browse(batch_ids)._recompute_packagings()
        env.invalidate_all()
