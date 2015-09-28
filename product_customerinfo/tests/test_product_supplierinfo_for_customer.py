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
        self.customer = self.env.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_4')
        self.pricelist = self.env.ref('product.list0')
        self.pricelist_item = self.pricelist_item_model.browse(
            self.env.ref('product.item0').id)
        self.pricelist_item.write({'base': -2})

    def test_product_supplierinfo_for_customer(self):
        cond = [('name', '=', self.customer.id)]
        supplierinfos = self.supplierinfo_model.search(cond)
        self.assertEqual(len(supplierinfos), 0,
                         "Error: Supplier found in Supplierinfo")
        cond = [('name', '=', self.customer.id)]
        customerinfos = self.supplierinfo_model.with_context(
            supplierinfo_type='customer').search(cond)
        self.assertNotEqual(len(customerinfos), 0,
                            "Error: Supplier not found in Supplierinfo")
        price_unit = self.pricelist_model.with_context(
            supplierinfo_type='customer').price_rule_get(
            self.product.id, 7, partner=self.customer.id)
        self.assertTrue(
            price_unit.get(self.pricelist.id, False),
            "Error: Price unit not found for customer")
        price = price_unit.get(self.pricelist.id, False)[0]
        self.assertEqual(price, 20.0,
                         "Error: Price not found for product and customer")
