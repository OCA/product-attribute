# -*- coding: utf-8 -*-
# © 2016  Olivier Laurent, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp.tests.common as common
from ..model.product_pricelist_item import FIXED_PRICE_TYPE


class TestProductPricelistFixedPrice(common.TransactionCase):

    def test_onchange_base_ext(self):
        """ Check for the value of 'base' field when changing the value of
            'base_ext' field:
            * for sale price list
            * for purchase price list
        """
        item_obj = self.env['product.pricelist.item']
        plv = self.env.ref('product.ver0')
        base_sale = item_obj._get_default_base({'type': 'sale'})
        vals = {
            'price_version_id': plv.id,
            'base_ext': base_sale,
        }

        # check for the 'base' field, it must be equal to base_ext=base_sale
        # when base_ext != -3
        item = item_obj.new(values=vals)
        item.change_base_ext()
        self.assertEqual(item.base, item.base_ext)
        self.assertEqual(item.base, base_sale)

        # force a fixed price
        vals['base_ext'] = FIXED_PRICE_TYPE

        # check again, it must be the same as default 'base' value
        item = item_obj.new(values=vals)
        item.change_base_ext()
        self.assertNotEqual(item.base, item.base_ext)
        self.assertEqual(item.base, base_sale)
        self.assertEqual(item.price_discount, -1.0)

        # change the type of the pricelist => purchase
        plv.pricelist_id.type = 'purchase'
        base_pur = item_obj._get_default_base({'type': 'purchase'})
        self.assertNotEqual(base_sale, base_pur)

        vals['base_ext'] = base_pur

        # check for the 'base' field, it must be equal to base_ext=base_pur
        item = item_obj.new(values=vals)
        item.change_base_ext()
        self.assertEqual(item.base, item.base_ext)
        self.assertEqual(item.base, base_pur)

        # force a fixed price
        vals['base_ext'] = FIXED_PRICE_TYPE

        # check again, it must be the same as default 'base' value
        item = item_obj.new(values=vals)
        item.change_base_ext()
        self.assertNotEqual(item.base, item.base_ext)
        self.assertEqual(item.base, base_pur)
        self.assertEqual(item.price_discount, -1.0)
