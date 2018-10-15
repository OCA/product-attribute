# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# Copyright 2018 Eficent
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestProductSupplierinfoForCustomer(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductSupplierinfoForCustomer, cls).setUpClass()
        cls.supplierinfo_model = cls.env['product.supplierinfo']
        cls.pricelist_item_model = cls.env['product.pricelist.item']
        cls.pricelist_model = cls.env['product.pricelist']
        cls.customer = cls._create_customer('customer1')
        cls.unknown = cls._create_customer('customer2')
        cls.product = cls.env.ref('product.product_product_4')
        cls.supplierinfo = cls._create_supplierinfo(
            'customer', cls.customer, cls.product)
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'currency_id': cls.env.ref('base.USD').id,
        })
        cls.company = cls.env.ref('base.main_company')
        cls.pricelist_item = cls.env['product.pricelist.item'].create({
            'applied_on': '1_product',
            'base': 'list_price',
            'name': 'Test Pricelist Item',
            'pricelist_id': cls.pricelist.id,
            'compute_price': 'fixed',
            'fixed_price': 100.0,
            'product_tmpl_id': cls.product.id,
        })

    @classmethod
    def _create_customer(cls, name):
        """Create a Partner."""
        return cls.env['res.partner'].create({
            'name': name,
            'email': 'example@yourcompany.com',
            'customer': True,
            'phone': 123456,
        })

    @classmethod
    def _create_supplierinfo(cls, supplierinfo_type, partner, product):
        return cls.env['product.supplierinfo'].create({
            'name': partner.id,
            'product_id': product.id,
            'product_code': '00001',
            'supplierinfo_type': supplierinfo_type,
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
        sup_info.write({'supplierinfo_type': 'customer'})
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

    def test_product_supplierinfo_price(self):
        price = self.product._get_price_from_supplierinfo(
            partner_id=self.customer.id)
        self.assertEqual(price, 100.0,
                         "Error: Price not found for product and customer")
        res = self.product.with_context(
            partner_id=self.customer.id).price_compute(
            'partner', self.product.uom_id, self.company.currency_id,
            self.company)
        self.assertEqual(
            res[self.product.id], 100.0,
            "Error: Wrong price for product and customer")
        res = self.product.with_context(
            partner_id=self.unknown.id).price_compute(
            'partner', self.product.uom_id, self.company.currency_id,
            self.company)
        self.assertEqual(
            res[self.product.id], 750.0,
            "Error: price does not match list price")
