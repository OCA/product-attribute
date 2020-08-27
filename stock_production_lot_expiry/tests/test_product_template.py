# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductTemplate, cls).setUpClass()
        cls.StockConfigSettings = cls.env["stock.config.settings"]
        cls.ProductCategory = cls.env["product.category"]
        cls.ProductCategory._parent_store_compute()
        cls.ProductProduct = cls.env["product.product"]
        cls.categ_lvl = cls.env.ref("product.product_category_all")
        cls.categ_lvl_1 = cls.ProductCategory.create(
            {"name": "level_1", "parent_id": cls.categ_lvl.id}
        )
        cls.categ_lvl_1_1 = cls.ProductCategory.create(
            {
                "name": "level_1_1",
                "parent_id": cls.categ_lvl_1.id,
                "specific_lot_expiry_field_name": "life_date",
            }
        )

        cls.categ_lvl_1_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1_1", "parent_id": cls.categ_lvl_1_1.id}
        )
        cls.default_expiry_field_name = (
            cls.StockConfigSettings.get_production_lot_expiry_date_field()
        )
        cls.product = cls.ProductProduct.create(
            {"name": "test product", "categ_id": cls.categ_lvl_1_1_1.id}
        )
        assert cls.default_expiry_field_name == "removal_date"

    def test_00(self):
        """
        Data:
            * A product without value for specific_lot_expiry_field_name and
              linked to a category at level 1_1_1
            * lot_expiry_field_name value on categ_lvl_1_1_1 is "life_date"
              (inherited from categ_lvl_1_1)
            * lot_expiry_field_name value on categ_lvl is the default one
            ("removal_date")
        Test case:
            1. Check the value for the field lot_expiry_field_name
            2. Linked the product to categ_lvl
            3. Check the value fot the field lot_expiry_field_name
        Expected result:
            1. value must be "life_date"
            3. value must be "removal_date"
        """
        self.assertEqual(self.product.lot_expiry_field_name, "life_date")
        self.product.categ_id = self.categ_lvl
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")

    def test_01(self):
        """
        Data:
            * A product without value for specific_lot_expiry_field_name and
              linked to a category at level 1_1_1
            * lot_expiry_field_name value on categ_lvl_1_1_1 is "life_date"
              (inherited from categ_lvl_1_1)
        Test case:
            1. Check the value for the field lot_expiry_field_name
            2. set the value 'removal_date' on the field
               pecific_lot_expiry_field_name
            3. Check the value fot the field lot_expiry_field_name
        Expected result:
            1. value must be "life_date"
            3. value must be "removal_date"
        """
        self.assertEqual(self.product.lot_expiry_field_name, "life_date")
        self.product.specific_lot_expiry_field_name = "removal_date"
        self.assertEqual(self.product.lot_expiry_field_name, "removal_date")
