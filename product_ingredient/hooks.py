# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def pre_init_hook(cr):
    """
    Create product_allergen_attribute used in compute methods with get_allergen_id()
    """
    openupgrade.load_data(cr, "product_ingredient", "data/product_allergen_data.xml")
