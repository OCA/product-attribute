# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def pre_init_hook(cr):
    """
    Create product_allergen_attribute to can be used in get_allergen_id() used in compute
    methods
    """
    openupgrade.load_data(cr, "product_ingredient", "data/product_allergen_data.xml")
