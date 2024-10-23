#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from .common import TestCommon


class TestProductTemplateAttributeValue(TestCommon):
    def test_formula_validation(self):
        """If the formula has a syntax error,
        it is raised when the formula changes."""
        new_formula = "import *"
        formula_ptav = self.formula_ptav

        with self.assertRaises(ValidationError) as ve:
            formula_ptav.extra_price_formula = new_formula
        exc_message = ve.exception.args[0]

        self.assertIn("invalid syntax", exc_message)

    def test_formula_copied(self):
        """The formula is copied from the attribute value."""
        # Arrange
        formula_product = self.formula_product
        formula_attribute_value = self.formula_attribute_value
        formula_ptav = formula_product.product_template_attribute_value_ids
        # pre-condition
        self.assertEqual(
            formula_ptav.product_attribute_value_id, formula_attribute_value
        )

        # Assert
        self.assertEqual(
            formula_ptav.extra_price_formula,
            formula_attribute_value.extra_price_formula,
        )

    def test_formula_no_back_propagate(self):
        """If the formula changes in the product template attribute value,
        it does not change in the product attribute value."""
        # Arrange
        new_formula = "price = 34"
        formula_product = self.formula_product
        formula_attribute_value = self.formula_attribute_value
        formula_ptav = formula_product.product_template_attribute_value_ids
        # pre-condition
        self.assertEqual(
            formula_ptav.product_attribute_value_id, formula_attribute_value
        )

        formula_ptav.extra_price_formula = new_formula

        # pre-condition
        self.assertNotEqual(
            formula_ptav.extra_price_formula,
            formula_attribute_value.extra_price_formula,
        )

    def test_formula_no_propagate(self):
        """If the formula changes in the product attribute value,
        it does not change in the product template attribute value."""
        # Arrange
        new_formula = "price = 34"
        formula_product = self.formula_product
        formula_attribute_value = self.formula_attribute_value
        formula_ptav = formula_product.product_template_attribute_value_ids
        # pre-condition
        self.assertEqual(
            formula_ptav.product_attribute_value_id, formula_attribute_value
        )

        formula_attribute_value.extra_price_formula = new_formula

        # pre-condition
        self.assertNotEqual(
            formula_ptav.extra_price_formula,
            formula_attribute_value.extra_price_formula,
        )
