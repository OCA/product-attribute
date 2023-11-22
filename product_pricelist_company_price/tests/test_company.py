#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestCompany(Common):
    def test_set_pricelist(self):
        """Set a pricelist in the company,
        the products prices are applied."""
        # Arrange
        company = self.company
        company.products_price_pricelist_id = False
        pricelist = self.pricelist
        product = self.product
        self._create_item(pricelist, product, 10)
        # pre-condition
        self.assertEqual(product.lst_price, 100)
        self.assertFalse(product.is_in_products_pricelist)

        # Act
        company.products_price_pricelist_id = pricelist

        # Assert
        self.assertEqual(product.lst_price, 10)
        self.assertFalse(
            product.is_in_products_pricelist, "No need to invalidate the cache"
        )
        product.invalidate_recordset(
            fnames=[
                "is_in_products_pricelist",
            ],
        )
        self.assertTrue(product.is_in_products_pricelist)
