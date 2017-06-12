# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class ProductCaseCopy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(ProductCaseCopy, self).setUp(*args, **kwargs)
        # Data Products
        self.prod = self.env.ref('product.product_product_5')

    def test_copy(self):
        prod_copy = self.prod.copy()
        self.assertFalse(prod_copy.product_customer_code_ids)
