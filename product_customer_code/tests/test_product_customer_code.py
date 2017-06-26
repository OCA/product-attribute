# coding: utf-8

from openerp.tests.common import TransactionCase


class TestProductCustomerCode(TransactionCase):
    """Test for product_customer_code:
        - Assign field product_customer_code_ids to product.
        - Test product name_search
    """
    def setUp(self):
        super(TestProductCustomerCode, self).setUp()
        self.product = self.env.ref('product.product_product_6')
        self.customer = self.env.ref('base.res_partner_9')

        self.product_cust_code_dict = {
            'product_code': 'Test',
            'partner_id': self.customer.id,
        }

    def test_10_find_product_customer_code(self):
        """Assign a product_customer_code to the product and then search it
        using name_search
        """
        self.product.write({
            'product_customer_code_ids':
            [(0, 0, self.product_cust_code_dict)]})
        self.assertTrue(self.product.product_customer_code_ids)

        context = {'partner_id': self.customer.id}
        product_names = self.product.with_context(
            context).name_search(name='Test')
        self.assertEquals(len(product_names), 1)
        product_id_found = product_names[0][0]
        self.assertEquals(self.product.id, product_id_found)

    def test_20_not_find_product_customer_code(self):
        """Can not find any product because the code does not exist in the
        product
        """
        self.assertFalse(self.product.product_customer_code_ids)

        context = {'partner_id': self.customer.id}
        product_names = self.product.with_context(
            context).name_search(name='Test')
        self.assertEquals(len(product_names), 0)
