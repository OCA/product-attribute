# -*- coding: utf-8 -*-
# © 2014 Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class ProductCaseNameSearch(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(ProductCaseNameSearch, self).setUp(*args, **kwargs)
        # Objects
        self.obj_product = self.env['product.product']

        # Data Category Product
        self.categ = self.ref('product.accessories')

        # Data UOM
        self.uom = self.ref('product.product_uom_unit')

        # Data Partner
        self.partner = self.ref('base.res_partner_3')

    def _prepare_product_data(self):
        data = {
            'name': 'Test Product - 1',
            'categ_id': self.categ,
            'standard_price': 500.0,
            'list_price': 150.5,
            'type': 'consu',
            'uom_id': self.uom,
            'uom_po_id': self.uom,
            'default_code': 'TST001',
            'product_customer_code_ids': [
                (0, 0, {'product_name': 'Test Product - 1',
                        'product_code': 'CUST001',
                        'partner_id': self.partner})
            ]
        }

        return data

    def _create_product(self):
        data = self._prepare_product_data()
        product = self.obj_product.create(data)

        return product

    def test_name_search(self):
        prod_id = self._create_product().id
        # Check Create Product
        self.assertIsNotNone(prod_id)

        # Check Name Search
        self.prod_ids = [prod_id]
        search_ids = self.obj_product.with_context(partner_id=self.partner).\
            name_search(
                name="CUST001",
                operator='ilike',
                args=[('id', 'in', self.prod_ids)])
        self.assertEqual(set([prod_id]), set([a[0] for a in search_ids]))
