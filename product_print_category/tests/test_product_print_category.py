# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductPrintCategory(TransactionCase):
    """Tests for 'Product Print Category' Module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductPrintWizard = cls.env["product.print.wizard"]
        cls.ProductProduct = cls.env["product.product"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.CustomReport = cls.env["report.product_print_category.report_pricetag"]
        cls.print_category_1 = cls.env.ref("product_print_category.demo_category_1")
        cls.print_category_2 = cls.env.ref("product_print_category.demo_category_2")

    # Test Section
    def test_01_product_product_to_print_value(self):
        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                    "print_category_id": self.print_category_1.id,
                }
            ]
        )
        self.assertEqual(product.to_print, True)

        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                }
            ]
        )
        self.assertEqual(product.to_print, False)

        product.print_category_id = self.print_category_1.id
        self.assertEqual(product.to_print, True)

        product.to_print = False
        product.name = "Demo Product Product Name Changed"
        self.assertEqual(product.to_print, True)

    def test_02_product_template_to_print_value(self):
        template = self.ProductTemplate.create(
            [
                {
                    "name": "Demo Product Product Name",
                    "print_category_id": self.print_category_1.id,
                }
            ]
        )
        self.assertEqual(template.to_print, True)

        template = self.ProductTemplate.create(
            [
                {
                    "name": "Demo Product Template Name",
                }
            ]
        )
        self.assertEqual(template.to_print, False)

        template.print_category_id = self.print_category_1.id
        self.assertEqual(template.to_print, True)

        template.to_print = False
        template.name = "Demo Product Template Name Changed"
        self.assertEqual(template.to_print, True)

    def test_10_test_wizard_obsolete(self):
        products = self.ProductProduct.search(
            [
                ("to_print", "=", True),
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        self.assertTrue(len(products) > 0)
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category_1.id],
        ).create([{}])
        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print obsolete product should propose 1 product",
        )

        wizard.print_report()
        self.env.ref("product_print_category.pricetag")._render_qweb_pdf(
            "product_print_category.report_pricetag",
            wizard.line_ids.ids,
        )

        products = self.ProductProduct.search(
            [
                ("to_print", "=", True),
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        self.assertTrue(len(products) == 0)

    def test_11_test_wizard_all(self):
        products = self.ProductProduct.search(
            [
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category_1.id],
            all_products=True,
        ).create({})

        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print all products should propose 3 products",
        )

    def test_21_onchange(self):
        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                }
            ]
        )
        self.assertEqual(product.print_category_id.id, False)

        # check rule with exact setting
        product.categ_id = self.env.ref("product.product_category_consumable")
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id, self.print_category_2)

        # Test with child category setting
        product.categ_id = self.env.ref("product.product_category_5")
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id, self.print_category_1)

        # Test if fallback settings works
        product.categ_id = self.env.ref("product.product_category_all")
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id.id, False)
