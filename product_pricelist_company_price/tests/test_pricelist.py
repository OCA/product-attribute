#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestPricelist(Common):
    def test_create_rule(self):
        """Create a rule for a product,
        the product's price is updated."""
        # Arrange
        company = self.company
        product = self.product
        pricelist = company.products_price_pricelist_id
        # pre-condition
        self.assertEqual(product.lst_price, 100)
        self.assertFalse(product.is_in_products_pricelist)

        # Act
        fixed_price = 10
        self._create_item(pricelist, product, fixed_price)

        # Assert
        self.assertEqual(product.lst_price, fixed_price)
        self.assertFalse(
            product.is_in_products_pricelist, "No need to invalidate the cache"
        )
        product.invalidate_recordset(
            fnames=[
                "is_in_products_pricelist",
            ],
        )
        self.assertTrue(product.is_in_products_pricelist)

    def test_create_template_rule(self):
        """Create a rule for a product template,
        the product's price is updated."""
        # Arrange
        company = self.company
        product = self.product.product_tmpl_id
        pricelist = company.products_price_pricelist_id
        # pre-condition
        self.assertEqual(product.list_price, 100)
        self.assertFalse(product.is_in_products_pricelist)

        # Act
        fixed_price = 10
        self._create_item(pricelist, product, fixed_price)

        # Assert
        self.assertEqual(product.list_price, fixed_price)
        self.assertFalse(
            product.is_in_products_pricelist, "No need to invalidate the cache"
        )
        product.invalidate_recordset(
            fnames=[
                "is_in_products_pricelist",
            ],
        )
        self.assertTrue(product.is_in_products_pricelist)

    def test_update_rule(self):
        """Update a rule for a product,
        the product's price is updated."""
        # Arrange
        company = self.company
        product = self.product
        pricelist = company.products_price_pricelist_id
        item = self._create_item(pricelist, product, 10)
        # pre-condition
        self.assertEqual(product.lst_price, 10)
        self.assertTrue(product.is_in_products_pricelist)

        # Act
        fixed_price = 20
        item.fixed_price = fixed_price

        # Assert
        self.assertEqual(product.lst_price, fixed_price)
