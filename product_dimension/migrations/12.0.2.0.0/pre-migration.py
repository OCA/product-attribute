# Copyright 2019 C2i Change 2 improve - Eduardo Magdalena <emagdalena@c2i.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

field_renames = [
    ("product.template", "product_template", "length", "product_length"),
    ("product.template", "product_template", "heigth", "product_heigth"),
    ("product.template", "product_template", "width", "product_width"),
]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.rename_fields(env, field_renames)
