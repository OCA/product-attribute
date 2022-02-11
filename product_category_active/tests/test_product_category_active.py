# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestProductCategoryActive(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        categ_obj = cls.env["product.category"]
        product_obj = cls.env["product.template"]
        cls.parent_categ = categ_obj.create({"name": "Parent category"})
        cls.child_1 = categ_obj.create(
            {"name": "child 1", "parent_id": cls.parent_categ.id}
        )
        cls.child_2 = categ_obj.create(
            {"name": "child 2", "parent_id": cls.parent_categ.id}
        )
        cls.product_1 = product_obj.create({"name": "Product 1"})

    def test_dont_archive_non_empty_categories(self):
        self.assertTrue(self.child_1.active)
        self.assertTrue(self.child_2.active)
        self.assertTrue(self.parent_categ.active)
        self.product_1.categ_id = self.child_1.id
        with self.assertRaises(ValidationError):
            self.parent_categ.active = False
        with self.assertRaises(ValidationError):
            (self.child_1 | self.child_2).write({"active": False})
        with self.assertRaises(ValidationError):
            self.child_1.active = False

    def test_archive_empty_categories(self):
        self.assertTrue(self.child_1.active)
        self.assertTrue(self.parent_categ.active)
        self.child_1.active = False
        self.parent_categ.active = False
        self.assertFalse(self.child_1.active)
        self.assertFalse(self.parent_categ.active)

    def test_archive_categories_with_inactive_products(self):
        self.assertTrue(self.child_1.active)
        self.assertTrue(self.child_1.active)
        self.assertTrue(self.parent_categ.active)
        self.product_1.categ_id = self.child_1.id
        self.product_1.active = False
        with self.assertRaises(ValidationError):
            self.parent_categ.active = False
        with self.assertRaises(ValidationError):
            self.child_1.active = False
