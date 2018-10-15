import odoo.tests.common as common


class TestProductSupplierinfoForCustomer(common.TransactionCase):

    def setUp(self):
        super(TestProductSupplierinfoForCustomer, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        self.customer = self.env.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')

    def test_product_supplierinfo_for_customer(self):
        cond = [('name', '=', self.customer.id)]
        supplierinfos = self.supplierinfo_model.search(cond)
        self.assertEqual(len(supplierinfos), 0,
                         "Error: Supplier found in Supplierinfo")
        customerinfos = self.supplierinfo_model.with_context(
            supplierinfo_type='customer').search(cond)
        self.assertNotEqual(len(customerinfos), 0,
                            "Error: Supplier not found in Supplierinfo")
