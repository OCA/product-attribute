# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openerp.api import Environment
from openerp import SUPERUSER_ID


def import_customer_code(env):
    env.cr.execute("""SELECT column_name
        FROM information_schema.columns
        WHERE table_name='product_customer_code'""")
    if env.cr.fetchone():
        env.cr.execute("""
            select product_id,
            product_code, partner_id, company_id, product_name
            from product_customer_code
        """)
        for product_id, product_code, partner_id, company_id, product_name in \
                env.cr.fetchall():
            pt_id = env['product.product'].browse(
                product_id).product_tmpl_id.id
            vals = {'name': partner_id,
                    'product_tmpl_id': pt_id,
                    'product_code': product_code,
                    'type': 'customer',
                    'pricelist_ids': [(
                        0, 0, {'price': 0.0, 'min_quantity': 0.0})],
                    }
            env['product.supplierinfo'].create(vals)


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    import_customer_code(env)
