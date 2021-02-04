# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestProductPricelistDirectPrint(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductPricelistDirectPrint, cls).setUpClass()
        cls.pricelist = cls.env.ref('product.list0')
        cls.category = cls.env['product.category'].create({
            'name': 'Test category',
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Product for test',
            'categ_id': cls.category.id,
            'default_code': 'TESTPROD01',
        })
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner for test',
            'property_product_pricelist': cls.pricelist.id,
            'email': 'test@test.com',
        })
        cls.wiz_obj = cls.env['product.pricelist.print']

    def test_defaults(self):
        wiz = self.wiz_obj.new()
        res = wiz.with_context(
            active_model='product.pricelist',
            active_id=self.pricelist.id,
        ).default_get([])
        self.assertEqual(res['pricelist_id'], self.pricelist.id)
        res = wiz.with_context(
            active_model='product.pricelist.item',
            active_ids=self.pricelist.item_ids.ids,
        ).default_get([])
        self.assertEqual(res['pricelist_id'], self.pricelist.id)
        res = wiz.with_context(
            active_model='res.partner',
            active_id=self.partner.id,
            active_ids=[self.partner.id],
        ).default_get([])
        self.assertEqual(
            res['pricelist_id'], self.partner.property_product_pricelist.id)
        res = wiz.with_context(
            active_model='product.template',
            active_ids=self.product.product_tmpl_id.ids,
        ).default_get([])
        self.assertEqual(
            res['product_tmpl_ids'][0][2], self.product.product_tmpl_id.ids)
        res = wiz.with_context(
            active_model='product.product',
            active_ids=self.product.ids,
        ).default_get([])
        self.assertEqual(
            res['product_ids'][0][2], self.product.ids)
        self.assertTrue(res['show_variants'])
        with self.assertRaises(ValidationError):
            wiz.print_report()
        wiz.show_sale_price = True
        res = wiz.print_report()
        self.assertIn('report_name', res)

    def test_action_pricelist_send_multiple_partner(self):
        partner_2 = self.env['res.partner'].create({
            'name': 'Partner for test 2',
            'property_product_pricelist': self.pricelist.id,
            'email': 'test2@test.com',
        })
        wiz = self.wiz_obj.with_context(
            active_model='res.partner',
            active_ids=[self.partner.id, partner_2.id],
        ).create({})
        wiz.action_pricelist_send()

    def test_show_only_defined_products(self):
        self.pricelist.item_ids.write({
            "applied_on": "0_product_variant",
            "product_id": self.product.id,
        })
        wiz = self.wiz_obj.with_context(
            active_model='product.pricelist',
            active_id=self.pricelist.id,
        ).create({})
        wiz.show_only_defined_products = True
        wiz.show_variants = True
        products = wiz.get_products_to_print()
        self.assertIn(products, self.pricelist.item_ids.mapped('product_id'))
        self.pricelist.item_ids.write({
            "applied_on": "2_product_category",
            "categ_id": self.category.id,
        })
        wiz.show_only_defined_products = True
        wiz.show_variants = True
        products = wiz.get_products_to_print()
        self.assertIn(self.product, products)

    def test_reports(self):
        wiz = self.wiz_obj.with_context(
            active_model='product.pricelist',
            active_id=self.pricelist.id,
        ).create({})
        # Print PDF
        report_name = 'product_pricelist_direct_print.action_report_product_pricelist'
        report_pdf = self.env.ref(report_name).render(wiz.ids)
        self.assertGreaterEqual(len(report_pdf[0]), 1)
        # Export XLSX
        report_name = 'product_pricelist_direct_print.product_pricelist_xlsx'
        report_xlsx = self.env.ref(report_name).render(wiz.ids)
        self.assertGreaterEqual(len(report_xlsx[0]), 1)
        self.assertEqual(report_xlsx[1], 'xlsx')
