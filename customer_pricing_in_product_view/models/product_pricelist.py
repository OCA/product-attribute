# -*- coding: utf-8 -*-
# © 2014 O4SB <http://o4sb.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    # pylint: disable=old-api7-method-defined
    def name_get(self, cr, uid, ids, context=None):
        """
        When using widget=selection the orm seems to take care of converting
        the id to a list, but when passing in context (even when passing as
        a list) it converts to an int, causing name_get to fail.  This function
        just converts a single id to a list and passes to super.
        :return: tuple of (id, name)
        """
        if isinstance(ids, int):
            ids = [ids]
        return super(ProductPricelist, self).name_get(cr, uid, ids,
                                                      context=context)
