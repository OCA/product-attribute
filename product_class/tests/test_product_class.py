# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from psycopg2 import IntegrityError

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestProductClass(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        # The class and attribute line fields live in the "Attributes &
        # Variants" page, only shown to users having the variants group.
        cls.env.user.group_ids += cls.env.ref("product.group_product_variant")
        cls.size_attr = cls.env["product.attribute"].create({"name": "Size"})
        cls.size_value = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.size_attr.id}
        )
        cls.color_attr = cls.env["product.attribute"].create({"name": "Color"})
        cls.color_value = cls.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": cls.color_attr.id}
        )

    def _create_product_attribute_line(self, product, attribute, values):
        return self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product.id,
                "attribute_id": attribute.id,
                "value_ids": [Command.set(values.ids)],
            }
        )

    def _make_class_attribute_line(self, attribute, required=False):
        return Command.create(
            {
                "attribute_id": attribute.id,
                "required": required,
            }
        )

    def _create_product_class(self, name, line_commands):
        return self.env["product.class"].create(
            {
                "name": name,
                "attribute_line_ids": line_commands,
            }
        )

    def test_product_with_compatible_class(self):
        """A product can use a class when its attributes match."""
        product_class = self._create_product_class(
            "Test Class",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        product = self.env["product.template"].create({"name": "Product 1"})
        self._create_product_attribute_line(product, self.size_attr, self.size_value)

        product.write({"class_id": product_class.id})

        self.assertEqual(product.class_id, product_class)

    def test_constraint_raises_on_incompatible_attribute_write(self):
        """A classed product cannot add attributes outside its class."""
        product_class = self._create_product_class(
            "Test Class 2", [self._make_class_attribute_line(self.size_attr)]
        )
        product = self.env["product.template"].create({"name": "Product 2"})
        self._create_product_attribute_line(product, self.size_attr, self.size_value)
        product.class_id = product_class

        with self.assertRaisesRegex(
            ValidationError, "do not belong to the selected class"
        ):
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.color_attr.id,
                                "value_ids": [Command.set([self.color_value.id])],
                            }
                        )
                    ]
                }
            )

    def test_constraint_raises_on_incompatible_class_change(self):
        """Changing to an incompatible class must raise a validation error."""
        color_class = self._create_product_class(
            "Color Class", [self._make_class_attribute_line(self.color_attr)]
        )
        product = self.env["product.template"].create({"name": "Product 3"})
        self._create_product_attribute_line(product, self.color_attr, self.color_value)
        product.class_id = color_class

        size_class = self._create_product_class(
            "Size Class", [self._make_class_attribute_line(self.size_attr)]
        )
        with self.assertRaisesRegex(
            ValidationError,
            "Please remove these attributes or change the product class",
        ):
            product.class_id = size_class

    def test_clearing_class_id_removes_constraint(self):
        """Removing class_id from a product allows any attribute afterwards."""
        product_class = self._create_product_class(
            "Size Only", [self._make_class_attribute_line(self.size_attr)]
        )
        product = self.env["product.template"].create({"name": "Product 5"})
        self._create_product_attribute_line(product, self.size_attr, self.size_value)
        product.class_id = product_class

        with self.assertRaisesRegex(
            ValidationError, "do not belong to the selected class"
        ):
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.color_attr.id,
                                "value_ids": [Command.set([self.color_value.id])],
                            }
                        )
                    ]
                }
            )

        product.class_id = False

        product.write(
            {
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color_attr.id,
                            "value_ids": [Command.set([self.color_value.id])],
                        }
                    )
                ]
            }
        )

    def test_class_with_no_attributes_rejects_any_attribute_line(self):
        """A class with no attributes prevents adding any attribute lines."""
        empty_class = self.env["product.class"].create({"name": "Empty Class"})
        product = self.env["product.template"].create(
            {"name": "Product 6", "class_id": empty_class.id}
        )

        with self.assertRaisesRegex(
            ValidationError, "do not belong to the selected class"
        ):
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.size_attr.id,
                                "value_ids": [Command.set([self.size_value.id])],
                            }
                        )
                    ]
                }
            )

    def test_classed_product_with_no_attribute_lines_is_valid(self):
        """A product with a class but no attribute lines is valid."""
        product_class = self._create_product_class(
            "Hammers", [self._make_class_attribute_line(self.size_attr)]
        )
        product = self.env["product.template"].create(
            {"name": "Product 7", "class_id": product_class.id}
        )
        self.assertEqual(product.class_id, product_class)
        self.assertFalse(product.attribute_line_ids)

    def test_cannot_remove_class_attribute_used_in_products(self):
        """Removing an attribute from class is forbidden if products still use it."""
        product_class = self._create_product_class(
            "Furniture Class",
            [
                self._make_class_attribute_line(self.size_attr),
                self._make_class_attribute_line(self.color_attr),
            ],
        )
        product_1 = self.env["product.template"].create(
            {"name": "Chair", "class_id": product_class.id}
        )
        product_2 = self.env["product.template"].create(
            {"name": "Table", "class_id": product_class.id}
        )
        self._create_product_attribute_line(product_1, self.size_attr, self.size_value)
        self._create_product_attribute_line(
            product_1, self.color_attr, self.color_value
        )
        self._create_product_attribute_line(
            product_2, self.color_attr, self.color_value
        )

        with self.assertRaisesRegex(
            ValidationError,
            "Please remove these attributes or change the product class",
        ):
            product_class.write(
                {
                    "attribute_line_ids": [
                        Command.clear(),
                        self._make_class_attribute_line(self.size_attr),
                    ]
                }
            )

    def test_attribute_classes_count_updates_from_linked_classes(self):
        """Attribute class counters reflect the linked product classes."""
        product_class = self._create_product_class(
            "Counted Class",
            [
                self._make_class_attribute_line(self.size_attr),
                self._make_class_attribute_line(self.color_attr),
            ],
        )

        self.assertEqual(self.size_attr.classes_count, 1)
        self.assertEqual(self.color_attr.classes_count, 1)

        product_class.write(
            {
                "attribute_line_ids": [
                    Command.clear(),
                    self._make_class_attribute_line(self.size_attr),
                ]
            }
        )

        self.assertEqual(self.size_attr.classes_count, 1)
        self.assertEqual(self.color_attr.classes_count, 0)

    def test_unique_name_constraint(self):
        """Creating two product classes with the same name raises an integrity error."""
        self.env["product.class"].create({"name": "Unique Class"})
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["product.class"].create({"name": "Unique Class"})

    def test_required_attributes_must_be_defined_on_products(self):
        """Products with class_id must define all required class attributes."""
        product_class = self._create_product_class(
            "Required Class",
            [
                self._make_class_attribute_line(self.size_attr, required=True),
                self._make_class_attribute_line(self.color_attr),
            ],
        )
        product = self.env["product.template"].create({"name": "Product 8"})
        self._create_product_attribute_line(product, self.color_attr, self.color_value)

        with self.assertRaisesRegex(
            ValidationError,
            "is missing required attributes for the selected class",
        ):
            product.class_id = product_class

    def test_required_attributes_accept_product_when_defined(self):
        """Products can be assigned to class when all required attributes exist."""
        product_class = self._create_product_class(
            "Required Class 2",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        product = self.env["product.template"].create({"name": "Product 9"})
        self._create_product_attribute_line(product, self.size_attr, self.size_value)

        product.class_id = product_class
        # No exception should be raised
        self.assertEqual(product.class_id, product_class)

    def test_product_prefills_required_class_attributes(self):
        """Picking a class on a product suggests its required attributes.

        Scenario:
            1. Create a class requiring one attribute and allowing another one.
            2. On a brand new product form, select that class.
        Expected:
            - Only the required attribute is added as a line.
            - No value is selected on it, so the user must fill it in.
        """
        product_class = self._create_product_class(
            "Prefill Class",
            [
                self._make_class_attribute_line(self.size_attr, required=True),
                self._make_class_attribute_line(self.color_attr),
            ],
        )
        form = Form(self.env["product.template"])
        form.class_id = product_class

        self.assertEqual(len(form.attribute_line_ids), 1)
        with form.attribute_line_ids.edit(0) as line:
            self.assertEqual(line.attribute_id, self.size_attr)
            self.assertFalse(line.value_ids)

    def test_saved_product_without_attributes_prefills_them(self):
        """Saved products without attributes are filled in as well.

        Scenario:
            1. Create and save a product without attributes.
            2. Select a class requiring an attribute on its form.
        Expected:
            - The required attribute is suggested, with no value selected.
        """
        product_class = self._create_product_class(
            "Prefill Saved Class",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        product = self.env["product.template"].create({"name": "Product 10"})

        form = Form(product)
        form.class_id = product_class

        self.assertEqual(len(form.attribute_line_ids), 1)
        with form.attribute_line_ids.edit(0) as line:
            self.assertEqual(line.attribute_id, self.size_attr)
            self.assertFalse(line.value_ids)

    def test_saved_product_with_attributes_is_not_prefilled(self):
        """Attributes of a saved product are left alone.

        Scenario:
            1. Create a product having one attribute with a value.
            2. Select a class requiring another attribute on its form.
        Expected:
            - The existing attribute is kept and nothing is suggested.
        """
        product_class = self._create_product_class(
            "Prefill Filled Class",
            [self._make_class_attribute_line(self.color_attr, required=True)],
        )
        product = self.env["product.template"].create({"name": "Product 11"})
        self._create_product_attribute_line(product, self.size_attr, self.size_value)

        form = Form(product)
        form.class_id = product_class

        self.assertEqual(len(form.attribute_line_ids), 1)
        with form.attribute_line_ids.edit(0) as line:
            self.assertEqual(line.attribute_id, self.size_attr)

    def test_clearing_class_drops_suggested_attributes(self):
        """Removing the class removes the attributes suggested for it.

        Scenario:
            1. On a new product form, select a class requiring one attribute.
            2. Without filling anything in, clear the class.
        Expected:
            - The suggested attribute line is removed.
        """
        product_class = self._create_product_class(
            "Cleared Class",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        form = Form(self.env["product.template"])
        form.class_id = product_class

        form.class_id = self.env["product.class"]

        self.assertFalse(form.attribute_line_ids)

    def test_switching_class_replaces_suggested_attributes(self):
        """Suggested attributes follow the class as long as they are untouched.

        Scenario:
            1. On a new product form, select a class requiring one attribute.
            2. Without filling anything in, select another class requiring a
               different attribute.
        Expected:
            - The first suggestion is dropped and replaced by the new one.
        """
        size_class = self._create_product_class(
            "Prefill Size Class",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        color_class = self._create_product_class(
            "Prefill Color Class",
            [self._make_class_attribute_line(self.color_attr, required=True)],
        )
        form = Form(self.env["product.template"])
        form.class_id = size_class

        form.class_id = color_class

        self.assertEqual(len(form.attribute_line_ids), 1)
        with form.attribute_line_ids.edit(0) as line:
            self.assertEqual(line.attribute_id, self.color_attr)

    def test_switching_class_keeps_filled_attributes(self):
        """Attributes the user filled in are never discarded.

        Scenario:
            1. On a new product form, select a class requiring one attribute.
            2. Pick a value on the suggested line.
            3. Select another class requiring a different attribute.
        Expected:
            - The filled line is kept as it is, and nothing is suggested for
              the new class.
        """
        size_class = self._create_product_class(
            "Keep Size Class",
            [self._make_class_attribute_line(self.size_attr, required=True)],
        )
        color_class = self._create_product_class(
            "Keep Color Class",
            [self._make_class_attribute_line(self.color_attr, required=True)],
        )
        form = Form(self.env["product.template"])
        form.class_id = size_class
        with form.attribute_line_ids.edit(0) as line:
            line.value_ids.add(self.size_value)

        form.class_id = color_class

        self.assertEqual(len(form.attribute_line_ids), 1)
        with form.attribute_line_ids.edit(0) as line:
            self.assertEqual(line.attribute_id, self.size_attr)
            self.assertEqual(list(line.value_ids), [self.size_value])

    def test_class_attribute_line_is_unique_per_class(self):
        """A class cannot configure the same attribute more than once."""
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self._create_product_class(
                "Duplicate Attr Class",
                [
                    self._make_class_attribute_line(self.size_attr),
                    self._make_class_attribute_line(self.size_attr),
                ],
            )
