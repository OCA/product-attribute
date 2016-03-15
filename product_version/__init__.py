# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from . import models


def set_active_product_active_state(cr, registry):
    """Set those active BoMs to state 'active'"""
    cr.execute("""UPDATE product_template
                    SET state = 'sellable'
                  WHERE active = True""")
