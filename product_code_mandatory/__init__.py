from . import models


def pre_init_product_code(env):
    env.cr.execute(
        """
        SELECT product_tmpl_id from product_product
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0
        GROUP BY product_tmpl_id
        HAVING COUNT(product_tmpl_id) = 1"""
    )
    product_template_ids = [x[0] for x in env.cr.fetchall()]
    env.cr.execute(
        """UPDATE product_product
        SET default_code = 'DEFAULT' || nextval('ir_default_id_seq')
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0"""
    )

    env["product.template"].browse(product_template_ids)._compute_default_code()

    return True
