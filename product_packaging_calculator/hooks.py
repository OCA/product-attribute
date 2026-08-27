# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openupgradelib import openupgrade as ou


def pre_init_hook(env):
    # Migrate from 'stock_packaging_calculator'
    if ou.is_module_installed(
        env.cr, "stock_packaging_calculator"
    ) and not ou.is_module_installed(env.cr, "product_packaging_calculator"):
        # NOTE: not using 'openupgrade.update_module_names' to keep the
        # 'stock_packaging_calculator' module entry available to not break
        # installations (modules could still depend on it)
        ou.update_module_moved_models(
            env.cr,
            "product.qty_by_packaging.mixin",
            "stock_packaging_calculator",
            "product_packaging_calculator",
        )
        ou.update_module_moved_models(
            env.cr,
            "product.product",
            "stock_packaging_calculator",
            "product_packaging_calculator",
        )
