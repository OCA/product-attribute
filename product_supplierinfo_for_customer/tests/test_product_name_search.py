# coding: utf-8

from openerp.tests.common import TransactionCase


class TestProductNameSearch(TransactionCase):
    """Test for:
        - Assign a configuration customer for product.
        - Test product name_search
    """
    def setUp(self):
        super(TestProductNameSearch, self).setUp()
        self.product = self.env['product.product'].create(
            {'name': 'Test product'})
        self.customer = self.env.ref('base.res_partner_9')
        self.supplierinfo = self.env['product.supplierinfo']

        self.supplierinfo_dict = {
            'product_code': 'test_123',
            'name': self.customer.id,
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'type': 'customer',
        }

    def test_10_find_product_customer_code(self):
        """Assign a product_supplierinfo to the product and then search it
        using name_search
        """
        self.supplierinfo.create(self.supplierinfo_dict)
        self.assertTrue(self.product.customer_ids)

        context = {'partner_id': self.customer.id,
                   'supplierinfo_type': 'customer'}
        product_names = self.product.with_context(
            context).name_search(name='test_123')
        self.assertEquals(len(product_names), 1)
        product_id_found = product_names[0][0]
        self.assertEquals(self.product.id, product_id_found)

    def test_20_not_find_product_customer_code(self):
        """Can not find any product because the supplierinfo does not exist
        """
        self.assertFalse(self.product.customer_ids)

        context = {'partner_id': self.customer.id,
                   'supplierinfo_type': 'customer'}
        product_names = self.product.with_context(
            context).name_search(name='test_123')
        self.assertEquals(len(product_names), 0)
