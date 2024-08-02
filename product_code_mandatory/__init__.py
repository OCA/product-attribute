from . import models


def pre_init_product_code(env):
    env.cr.execute(
        """UPDATE product_template
        SET default_code = 'DEFAULT' || nextval('ir_default_id_seq')
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0"""
    )
    env.cr.execute(
        """UPDATE product_product
        SET default_code = 'DEFAULT' || nextval('ir_default_id_seq')
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0"""
    )
    return True
