#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import TestCommon


class TestProduct(TestCommon):
    def test_formula_evaluation(self):
        """The formula is evaluated correctly."""
        # Arrange
        formula_price = self.formula_price
        formula_product = self.formula_product
        formula_ptav = self.formula_ptav
        # pre-condition
        self.assertIn(
            formula_ptav, formula_product.product_template_attribute_value_ids
        )

        # Assert
        self.assertEqual(formula_product.lst_price, formula_price)

    def test_formula_change(self):
        """If the formula changes in product template attribute value,
        the new formula is evaluated."""
        # Arrange
        formula_price = self.formula_price
        new_formula_price = 34
        new_formula = "price = %s" % new_formula_price
        formula_product = self.formula_product
        formula_ptav = formula_product.product_template_attribute_value_ids
        formula_ptav.extra_price_formula = new_formula
        formula_attribute_value = self.formula_attribute_value
        # pre-condition
        self.assertNotEqual(formula_price, new_formula_price)
        self.assertIn(formula_attribute_value, formula_ptav.product_attribute_value_id)

        # Assert
        self.assertEqual(formula_product.lst_price, new_formula_price)
