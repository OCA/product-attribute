#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from .common import TestCommon


class TestProductAttributeValue(TestCommon):
    def test_formula_validation(self):
        """If the formula has a syntax error,
        it is raised when the formula changes."""
        new_formula = "import *"
        formula_attribute_value = self.formula_attribute_value

        with self.assertRaises(ValidationError) as ve:
            formula_attribute_value.extra_price_formula = new_formula
        exc_message = ve.exception.args[0]

        self.assertIn("invalid syntax", exc_message)
