# Copyright 2019 Eficent <http://www.eficent.com>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _move_model_in_data(env, ids, old_model, new_model):
    renames = [
        ('mail_message', 'model', 'res_id'),
        ('mail_followers', 'res_model', 'res_id'),
        ('ir_attachment', 'res_model', 'res_id'),
        ('mail_activity', 'res_model', 'res_id'),
        ('ir_model_data', 'model', 'res_id'),
    ]
    for rename in renames:
        openupgrade.logged_query(
            env.cr, """
            UPDATE {A}
            SET {B} = '{C}'
            WHERE {D} IN {E} AND {F} = '{G}'""".format(
                A=rename[0],
                B=rename[1], C=new_model,
                D=rename[2], E=tuple(ids), F=rename[1], G=old_model,
            ),
        )


def fill_product_customerinfo(env):
    cr = env.cr
    openupgrade.logged_query(
        cr, """
            CREATE TABLE product_customerinfo
            (LIKE product_supplierinfo INCLUDING ALL)""",
    )
    openupgrade.logged_query(
        cr, """
        INSERT INTO product_customerinfo
        SELECT *
        FROM product_supplierinfo
        WHERE supplierinfo_type = 'customer'
        RETURNING id""",
    )
    ids = [x[0] for x in cr.fetchall()]
    if ids:
        _move_model_in_data(
            env, ids, 'product.supplierinfo', 'product.customerinfo')
        cr.execute("CREATE SEQUENCE IF NOT EXISTS product_customerinfo_id_seq")
        cr.execute("SELECT setval('product_customerinfo_id_seq', "
                   "(SELECT MAX(id) FROM product_customerinfo))")
        cr.execute("ALTER TABLE product_customerinfo ALTER id "
                   "SET DEFAULT NEXTVAL('product_customerinfo_id_seq')")
        openupgrade.logged_query(
            cr, """
            DELETE
            FROM product_supplierinfo
            WHERE supplierinfo_type = 'customer'""",
        )


@openupgrade.migrate()
def migrate(env, version):
    fill_product_customerinfo(env)
