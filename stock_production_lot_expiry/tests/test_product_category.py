# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductCategory(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductCategory, cls).setUpClass()
        cls.StockConfigSettings = cls.env["stock.config.settings"]
        cls.ProductCategory = cls.env["product.category"]
        cls.ProductCategory._parent_store_compute()
        cls.categ_lvl = cls.env.ref("product.product_category_all")
        cls.categ_lvl_1 = cls.ProductCategory.create(
            {"name": "level_1", "parent_id": cls.categ_lvl.id}
        )
        cls.categ_lvl_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1", "parent_id": cls.categ_lvl_1.id}
        )

        cls.categ_lvl_1_1_1 = cls.ProductCategory.create(
            {"name": "level_1_1_1", "parent_id": cls.categ_lvl_1_1.id}
        )
        cls.default_expiry_field_name = (
            cls.StockConfigSettings.get_production_lot_expiry_date_field()
        )
        assert cls.default_expiry_field_name == "removal_date"

    def modify_config_expiry_field_name(self, field_name):
        self.StockConfigSettings.create(
            {"production_lot_expiry_date_field": field_name}
        ).execute()

    def test_00(self):
        """
        Data:
            A 3 depths category hierarchy without
            specific_lot_expiry_field_name
        Test Case:
            1. Read the lot_expiry_field_name at the deeper level
            2. Modify the field_name into the config
            3. Read the lot_expiry_field_name at the deeper level
        Expected result:
            1. The value is the default one specified into the config
            2. The value is the modified one
        """
        self.assertEqual(
            self.default_expiry_field_name,
            self.categ_lvl_1_1_1.lot_expiry_field_name,
        )
        self.modify_config_expiry_field_name("life_date")
        self.assertEqual(
            "life_date", self.categ_lvl_1_1_1.lot_expiry_field_name
        )

    def test_01(self):
        """
        Data:
            A 3 depths category hierarchy without
            specific_lot_expiry_field_name
        Test Case:
            1. Specify a specific_lot_expiry_field_name at level_1_1
        Expected result:
            The value at root level and level 1 is the default one
            specified into the config
            The value at level_1_1 and level_1_1_1 is the new one
        """
        self.categ_lvl_1_1.specific_lot_expiry_field_name = "life_date"
        self.assertEqual(
            self.default_expiry_field_name,
            self.categ_lvl.lot_expiry_field_name,
        )
        self.assertEqual(
            self.default_expiry_field_name,
            self.categ_lvl_1.lot_expiry_field_name,
        )
        self.assertEqual(
            "life_date", self.categ_lvl_1_1.lot_expiry_field_name
        )
        self.assertEqual(
            "life_date", self.categ_lvl_1_1_1.lot_expiry_field_name
        )

    def test_02(self):
        """
        Data:
            A 3 depths category hierarchy without
            specific_lot_expiry_field_name
        Test Case:
            1. Specify a specific_lot_expiry_field_name at root level
        Expected result:
            The value at each level must modified.
        """
        self.categ_lvl.specific_lot_expiry_field_name = "life_date"
        children = self.categ_lvl.child_id

        def check_field(categs, name):
            for categ in categs:
                self.assertEqual(
                    name,
                    categ.lot_expiry_field_name,
                    "Wrong expiry field name on categ %s" % categ.name,
                )
                check_field(categ.child_id, name)

        check_field(children, "life_date")
