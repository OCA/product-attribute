# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super().setUp()

        self.product_template_incl = self.env.ref(
            "product_sale_tax_price_included.product_template_incl")
        self.product_template_excl = self.env.ref(
            "product_sale_tax_price_included.product_template_excl")
        self.product_template_mixed = self.env.ref(
            "product_sale_tax_price_included.product_template_mixed")
        self.product_template_no_tax = self.env.ref(
            "product_sale_tax_price_included.product_template_no_tax")
        # if other accounting module are installed,
        # a default vat is set to the module. We remove it explicitely
        self.product_template_no_tax.taxes_id = False

    def test_product_template_incl(self):
        # 20% VAT Incl
        self.assertEquals(
            self.product_template_incl.price_vat_excl, 83.33)
        self.assertEquals(
            self.product_template_incl.price_vat_incl, 100.0)

    def test_product_template_excl(self):
        # 10% VAT Excl
        self.assertEquals(
            self.product_template_excl.price_vat_excl, 100.0)
        self.assertEquals(
            self.product_template_excl.price_vat_incl, 110.0)

    def test_product_template_mixed(self):
        # 20% VAT Incl + 10 VAT Excl
        self.assertEquals(
            self.product_template_mixed.price_vat_excl, 83.33)
        # The VAT Excl = 83.33 + 30%
        self.assertEquals(
            self.product_template_mixed.price_vat_incl, 108.33)

    def test_product_template_no_tax(self):
        self.assertEquals(
            self.product_template_no_tax.price_vat_excl, 100.0)
        self.assertEquals(
            self.product_template_no_tax.price_vat_incl, 100.0)
