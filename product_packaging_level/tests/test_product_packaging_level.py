# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestProductPackagingLevel(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("base.lang_fr").active = True

        cls.default_level = cls.env.ref(
            "product_packaging_level.product_packaging_level_default"
        )
        cls.level = cls.env["product.packaging.level"].create(
            {
                "name": "Packaging Level Test",
                "code": "TEST2",
                "sequence": 2,
            }
        )

        cls.level_fr = cls.env["product.packaging.level"].create(
            {
                "name": "Packaging Level Test",
                "code": "TEST3",
                "sequence": 2,
                "default_lang_id": cls.env.ref("base.lang_fr").id,
            }
        )
        cls.level_fr.with_context(lang="fr_FR").name = "Packaging Level Test France"
        cls.packaging_default = cls.env["product.packaging"].create(
            {"name": "Packaging Default", "qty": 1.0}
        )
        cls.packaging = cls.env["product.packaging"].create(
            {"name": "Packaging Test", "packaging_level_id": cls.level.id, "qty": 1.0}
        )
        cls.packaging_fr = cls.env["product.packaging"].create(
            {
                "name": "Packaging Test",
                "packaging_level_id": cls.level_fr.id,
                "qty": 1.0,
            }
        )
        cls.product = cls.env["product.template"].create(
            {"name": "Product Test", "packaging_ids": [(6, 0, cls.packaging.ids)]}
        )
        cls.package_type_pallet = cls.env.ref("stock.package_type_01")
        cls.package_type_box = cls.env.ref("stock.package_type_02")

    def test_packaging_default_level(self):
        self.assertEqual(self.default_level, self.packaging_default.packaging_level_id)

    def test_display_name(self):
        self.assertEqual(self.default_level.display_name, "Default Level (DEFAULT)")

    def test_name_by_level(self):
        self.packaging.name_policy = "by_package_level"
        self.assertEqual(self.packaging.name, "Packaging Level Test (TEST2)")
        self.assertEqual(self.packaging.display_name, "Packaging Level Test (TEST2)")
        self.packaging_fr.name_policy = "by_package_level"
        self.assertEqual(self.packaging_fr.name, "Packaging Level Test France (TEST3)")
        self.assertEqual(
            self.packaging_fr.display_name, "Packaging Level Test France (TEST3)"
        )

    def test_name_by_package_type(self):
        # Required for `package_type_id` to be visible in the view
        self.env.user.write(
            {"groups_id": [(4, self.env.ref("stock.group_tracking_lot").id)]}
        )
        self.packaging.name_policy = "by_package_type"
        self.packaging.package_type_id = self.package_type_box
        self.assertEqual(self.packaging.name, "Box")

    def test_name_by_user_defined(self):
        # Required for `package_type_id` to be visible in the view
        self.env.user.write(
            {"groups_id": [(4, self.env.ref("stock.group_tracking_lot").id)]}
        )
        packaging_name = "user defined - not box - not pallet"
        self.packaging.packaging_level_id.name_policy = "user_defined"
        self.packaging.name = packaging_name
        # try to change package_type_id
        self.packaging.package_type_id = self.package_type_box
        self.assertEqual(self.packaging.name, packaging_name)

        # try to change packaging level
        self.packaging.packaging_level_id = self.level
        self.assertEqual(self.packaging.name, packaging_name)

    def test_name_by_package_type_without_group_tracking_lot(self):
        # remove Packages from Internal group
        internal_group = self.env.ref("base.group_user")
        group_tracking_lot = self.env.ref("stock.group_tracking_lot")
        internal_group.implied_ids -= group_tracking_lot
        self.env.user.groups_id -= group_tracking_lot
        with self.assertRaises(ValidationError):
            self.packaging.packaging_level_id.write({"name_policy": "by_package_type"})

    def test_default_packaging_level_defined_on_package_type(self):
        self.package_type_box.packaging_level_id = self.default_level
        # check current level
        self.assertEqual(self.packaging.packaging_level_id, self.level)
        # set package_type and
        # recheck new level if same as level on package_type
        self.packaging.package_type_id = self.package_type_box
        self.packaging._onchange_package_type()
        self.assertEqual(self.packaging.packaging_level_id, self.default_level)

    def test_product_level_constraint(self):
        # Add a new packaging to product with same level as the other one.
        # Check that exception is raised
        with self.assertRaises(
            ValidationError, msg="It is forbidden to have different packagings"
        ):
            self.product.write(
                {
                    "packaging_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Packaging Test 2",
                                "packaging_level_id": self.level.id,
                            },
                        )
                    ]
                }
            )

    def test_packaging_required_gtin(self):
        # Check if the barcode required for gtin is well computed
        self.assertFalse(self.product.packaging_ids.barcode_required_for_gtin)
        self.level.has_gtin = True
        self.assertTrue(self.product.packaging_ids.barcode_required_for_gtin)

    def test_packaging_is_default(self):
        # Check that the 'is_default' value is set once
        msg = "There must be one product packaging level set as 'Is Default'."
        with self.assertRaises(ValidationError, msg=msg):
            self.default_level.is_default = False
        msg = "Only one product packaging level can be set as 'Is Default'."
        with self.assertRaises(ValidationError, msg=msg):
            self.level.is_default = True

    def test_packaging_qty_per_level(self):
        # Check if the barcode required for gtin is well computed
        self.level_3 = self.env["product.packaging.level"].create(
            {
                "name": "Packaging Level 3 Test",
                "code": "TEST3",
                "sequence": 3,
            }
        )
        self.packaging_3 = self.env["product.packaging"].create(
            {
                "name": "Packaging Test",
                "packaging_level_id": self.level_3.id,
                "qty": 3.0,
                "product_id": self.product.product_variant_ids.id,
            }
        )

        self.level_4 = self.env["product.packaging.level"].create(
            {
                "name": "Packaging Level 4 Test",
                "code": "TEST4",
                "sequence": 4,
            }
        )
        self.packaging_10 = self.env["product.packaging"].create(
            {
                "name": "Packaging Test",
                "packaging_level_id": self.level_4.id,
                "qty": 6.0,
                "product_id": self.product.product_variant_ids.id,
            }
        )

        self.assertEqual(self.packaging_3.qty_per_level, "3.0 TEST2")

        self.assertEqual(self.packaging_10.qty_per_level, "6.0 TEST2; 2.0 TEST3")
        # Base packaging has no qty per level
        self.assertEqual(self.packaging.qty_per_level, "")
