from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestProductMultiCategory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        ProductTemplate = cls.env["product.template"]
        ProductCategory = cls.env["product.category"]

        # Create default and classification categories
        cls.default_category = ProductCategory.create({"name": "Default Category"})
        cls.classification_category_1 = ProductCategory.create(
            {"name": "Classification Category 1"}
        )
        cls.classification_category_2 = ProductCategory.create(
            {"name": "Classification Category 2"}
        )

        # Create a product with the default category
        cls.product = ProductTemplate.create(
            {
                "name": "Multi-Category Test Product",
                "categ_id": cls.default_category.id,
            }
        )

    def _assign_classification_categories(self):
        """Assign additional classification categories to the product"""
        self.product.categ_ids = [
            Command.set(
                [
                    self.classification_category_1.id,
                    self.classification_category_2.id,
                ]
            )
        ]

    def test_assign_classification_categories(self):
        """Test that both classification categories can be
        assigned to a product."""
        self._assign_classification_categories()
        self.assertEqual(
            self.product.categ_ids,
            self.classification_category_1 | self.classification_category_2,
            "Product should have both classification categories assigned",
        )

    def test_remove_classification_category(self):
        """Test removing one classification category
        without affecting the other."""
        self._assign_classification_categories()
        self.product.categ_ids = [Command.unlink(self.classification_category_1.id)]
        self.assertEqual(
            self.product.categ_ids,
            self.classification_category_2,
            "Product should have only the remaining classification category",
        )

    def test_default_category_unchanged(self):
        """Ensure that the default category remains unchanged after
        assigning classification categories."""
        self._assign_classification_categories()
        self.assertEqual(
            self.product.categ_id,
            self.default_category,
            "Default category should remain unchanged",
        )
