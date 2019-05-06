# -*- coding: utf-8 -*-
# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestProductStockState(TransactionCase):
    def setUp(self):
        super(TestProductStockState, self).setUp()
        self.company = self.env.ref("base.main_company")
        self.category = self.env.ref("product.product_category_1")
        self.product_by_company = self.env.ref(
            "product_stock_state.product_setting_by_company"
        )
        self.product_by_categ_direct = self.env.ref("stock.product_icecream")
        self.product_by_categ_inherit = self.env.ref(
            "product.product_order_01"
        )
        self.product_by_product = self.env.ref(
            "product_stock_state.product_setting_by_product"
        )

    def test_01_global_product(self):
        """Test Global Settings"""
        self.assertEqual(
            self.product_by_company._get_stock_state_threshold(),
            self.company.stock_state_threshold,
        )

    def test_02_category_setting_direct(self):
        """Test Category Setting (Setting on the product category)"""
        self.assertEqual(
            self.product_by_categ_direct._get_stock_state_threshold(),
            self.category.stock_state_threshold,
        )

    def test_03_category_setting_inherit(self):
        """Test Category Setting (Setting on a parent category)"""
        self.assertEqual(
            self.product_by_categ_inherit._get_stock_state_threshold(),
            self.category.stock_state_threshold,
        )

    def test_04_category_setting_inherit(self):
        """Test Product Setting (Setting on a product unique template)"""
        self.assertEqual(
            self.product_by_product._get_stock_state_threshold(), 30
        )

    def test_05_state_out_of_stock(self):
        """Test Stock State computation"""
        self.assertEqual(self.product_by_product.stock_state, "out_of_stock")
