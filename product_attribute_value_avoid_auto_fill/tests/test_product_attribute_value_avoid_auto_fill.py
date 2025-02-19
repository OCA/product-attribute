# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestProductAttributeValueAutoFillOption(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute_01 = cls.create_attribute("Attribute 01", "no_variant", True)
        cls.attribute_02 = cls.create_attribute("Attribute 02", "no_variant", False)
        cls.product = cls.env["product.template"].create({"name": "Test"})

    @classmethod
    def create_attribute(cls, name, create_variant, avoid_fill_values):
        return cls.env["product.attribute"].create(
            {
                "name": name,
                "create_variant": create_variant,
                "avoid_fill_all_values": avoid_fill_values,
                "value_ids": [
                    Command.create(
                        {
                            "name": "Value 01",
                        }
                    ),
                    Command.create(
                        {
                            "name": "Value 02",
                        }
                    ),
                    Command.create(
                        {
                            "name": "Value 03",
                        }
                    ),
                ],
            }
        )

    def test_select_attributes_no_variant(self):
        # Checking attribute no_variant by default odoo selects all values.
        # But when avoid_fill_all_values is selected, ValidationError
        # should be raised when trying to save without selecting
        # any value. If it is selected, the values should be set
        with self.assertRaises(ValidationError):
            product_form = Form(self.product)
            with product_form.attribute_line_ids.new() as ptal_form:
                ptal_form.attribute_id = self.attribute_01
            product_form.save()
        product_form = Form(self.product)
        with product_form.attribute_line_ids.new() as ptal_form:
            ptal_form.attribute_id = self.attribute_02
        product_form.save()
        self.assertEqual(
            len(
                self.product.attribute_line_ids.filtered(
                    lambda p: p.attribute_id == self.attribute_02
                ).value_ids
            ),
            3,
        )
