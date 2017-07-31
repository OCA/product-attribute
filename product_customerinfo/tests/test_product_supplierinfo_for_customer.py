# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
import openerp.tests.common as common


class TestProductSupplierinfoForCustomer(common.TransactionCase):

    def setUp(self):
        super(TestProductSupplierinfoForCustomer, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        self.pricelist_item_model = self.env['product.pricelist.item']
        self.pricelist_model = self.env['product.pricelist']
        self.customer = self._create_customer('customer1')
        self.product = self.env.ref('product.product_product_4')
        self.supplierinfo = self._create_supplierinfo(
            'customer', self.customer, self.product)
        self.pricelist = self.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'currency_id': self.env.ref('base.USD').id,
        })
        self.pricelist_item = self.env['product.pricelist.item'].create({
            'applied_on': '1_product',
            'base': 'list_price',
            'name': 'Test Pricelist Item',
            'pricelist_id': self.pricelist.id,
            'compute_price': 'fixed',
            'fixed_price': 100.0,
            'product_tmpl_id': self.product.id,
            'sequence': 5,
        })

    def _create_customer(self, name):
        """Create a Partner."""
        return self.env['res.partner'].create({
            'name': name,
            'email': 'example@yourcompany.com',
            'customer': True,
            'phone': 123456,
        })

    def _create_supplierinfo(self, type, partner, product):
        return self.env['product.supplierinfo'].create({
            'name': partner.id,
            'product_id': product.id,
            'product_code': '00001',
            'type': type,
            'price': 100.0,
        })

    def test_default_get(self):
        """ checking values returned by default_get() """
        fields = ['name']
        values = self.customer.with_context(
            select_type=True).default_get(fields)
        self.assertEqual(values['customer'], False, "Incorrect default")

    def test_onchange_type(self):
        sup_info = self._create_supplierinfo(
            'supplier', self.customer, self.product)
        res = sup_info.onchange_type()
        domain = res.get('domain', False)
        name_dom = domain.get('name', False)
        self.assertEqual(name_dom, [('supplier', '=', True)])
        sup_info.write({'type': 'customer'})
        res = sup_info.onchange_type()
        domain = res.get('domain', False)
        name_dom = domain.get('name', False)
        self.assertEqual(name_dom, [('customer', '=', True)])

    def test_product_supplierinfo_for_customer(self):
        cond = [('name', '=', self.customer.id)]
        supplierinfos = self.supplierinfo_model.search(cond)
        self.assertEqual(len(supplierinfos), 0,
                         "Error: Supplier found in Supplierinfo")
        cond = [('name', '=', self.customer.id)]
        customerinfos = self.supplierinfo_model.with_context(
            supplierinfo_type='customer').search(cond)
        self.assertNotEqual(len(customerinfos), 0,
                            "Error: Customer not found in Supplierinfo")
        price_unit = self.pricelist_model.price_rule_get(
            self.product.id, 1, partner=self.customer.id)
        self.assertTrue(
            price_unit.get(self.pricelist.id, False),
            "Error: Price unit not found for customer")
        price = price_unit.get(self.pricelist.id, False)[0]
        self.assertEqual(price, 100.0,
                         "Error: Price not found for product and customer")
