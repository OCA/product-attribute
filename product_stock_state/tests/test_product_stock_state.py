# Copyright 2017-Today GRAP (http://www.grap.coop).
# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductStockState(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        # Create categories locally
        cls.category_saleable = cls.env["product.category"].create(
            {
                "name": "Test Saleable",
                "manual_stock_state_threshold": 10,
            }
        )
        cls.category_furniture = cls.env["product.category"].create(
            {
                "name": "Test Furniture",
                "parent_id": cls.category_saleable.id,
            }
        )
        cls.category_no_threshold = cls.env["product.category"].create(
            {
                "name": "Test No Threshold",
            }
        )
        # Create products locally
        cls.product_chair = cls.env["product.product"].create(
            {
                "name": "Test Chair",
                "categ_id": cls.category_furniture.id,
                "type": "consu",
            }
        )
        cls.product_threshold_on_company = cls.env["product.product"].create(
            {
                "name": "Test Product Company Threshold",
                "categ_id": cls.category_saleable.id,
                "type": "consu",
                "company_id": cls.company.id,
            }
        )
        cls.product_threshold_on_product = cls.env["product.product"].create(
            {
                "name": "Test Product Manual Threshold",
                "categ_id": cls.category_saleable.id,
                "type": "consu",
                "manual_stock_state_threshold": 30,
            }
        )
        cls.product_no_threshold = cls.env["product.product"].create(
            {
                "name": "Test Product No Threshold",
                "categ_id": cls.category_no_threshold.id,
                "type": "consu",
            }
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
        self.assertEqual(self.product_threshold_on_product.stock_state, "out_of_stock")

    def test_06_company_fallback(self):
        """Test fallback to company threshold"""
        self.assertEqual(
            self.product_no_threshold._get_stock_state_threshold(),
            self.company.stock_state_threshold,
        )
