# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    field_spec = [
        ("product_manufacturer", "product_template", "manufacturer", "manufacturer_id"),
        ("product_manufacturer", "product_product", "manufacturer", "manufacturer_id"),
    ]
    openupgrade.rename_fields(env=env, field_spec=field_spec, no_deep=True)
