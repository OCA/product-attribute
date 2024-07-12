# Copyright 2017-Today GRAP (http://www.grap.coop).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductStockState(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.ref("base.main_company")
        self.category_furniture = self.env.ref("product.product_category_5")
        self.category_saleable = self.env.ref("product.product_category_1")
        self.product_chair = self.env.ref("product.product_product_12")
        self.product_threshold_on_company = self.env.ref(
            "product_stock_state.product_setting_by_company"
        )
        self.product_threshold_on_product = self.env.ref(
            "product_stock_state.product_setting_by_product"
        )

    def test_01_global_product(self):
        """Test Global Settings"""
        self.assertEqual(
            self.product_threshold_on_company._get_stock_state_threshold(),
            self.company.stock_state_threshold,
        )

    def test_02_category_setting_direct(self):
        """Test Category Setting (Setting on the product category)"""
        self.category_furniture.stock_state_threshold = 77
        self.assertEqual(
            self.product_chair._get_stock_state_threshold(),
            self.category_furniture.stock_state_threshold,
        )

    def test_03_category_setting_inherit(self):
        """Test Category Setting (Setting on a parent category)"""
        self.assertEqual(
            self.product_chair._get_stock_state_threshold(),
            self.category_saleable.stock_state_threshold,
        )

    def test_04_category_setting_inherit(self):
        """Test Product Setting (Setting on a product unique template)"""
        self.assertEqual(
            self.product_threshold_on_product._get_stock_state_threshold(), 30
        )

    def test_05_state_out_of_stock(self):
        """Test Stock State computation"""
        self.assertEqual(
            self.product_threshold_on_product.stock_state, "out_of_stock"
        )
