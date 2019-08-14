# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, [
        ('product.template', 'product_template', 'pack', 'pack_ok')
    ])
    openupgrade.add_fields(env, [
        ('pack_type', 'product.template',
         'product_template', 'char', False, 'product_template'),
        ('pack_modifiable', 'product.template',
         'product_template', 'boolean', False, 'product_template'),
    ])
    openupgrade.logged_query(
        env.cr, """
            UPDATE product_template
            SET pack_type = (
                    CASE
                        WHEN pack_price_type = 'none_detailed_assited_price'
                            THEN NULL
                        WHEN pack_price_type = 'totalice_price'
                            THEN 'totalized_price'
                        WHEN pack_price_type = 'none_detailed_totaliced_price'
                            THEN 'none_detailed_totalized_price'
                        ELSE
                            pack_price_type
                    END
                ),
                pack_modifiable = (
                    CASE
                        WHEN allow_modify_pack in ('only_backend',
                                                  'frontend_backend')
                            THEN TRUE
                        ELSE
                            FALSE
                    END
                )
            """,
    )
