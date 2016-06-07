# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init_hook(cr, registry):
    """Make sure that after updating database tables for this module,
    existing values in pricelist item are set correctly."""
    cr.execute(
        "update product_pricelist_item"
        " set base_ext = base"
        " where base_ext != -3 and base != base_ext"
    )
