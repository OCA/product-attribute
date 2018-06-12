# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models


def pre_init_product_code(cr):
    cr.execute("""UPDATE product_template
        SET default_code = 'DEFAULT' || nextval('ir_default_id_seq')
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0""")
    cr.execute("""UPDATE product_product
        SET default_code = 'DEFAULT' || nextval('ir_default_id_seq')
        WHERE default_code is NULL
        OR LENGTH(default_code) = 0""")
    return True
