# Copyright Cetmix OU 2025
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install", "test_product_attribute")
class TestProductAttribute(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_attribute = cls.env["product.attribute"]
        cls.product_attribute_value = cls.env["product.attribute.value"]
        cls.product_template = cls.env["product.template"]

        cls.product_attribute_year = cls.product_attribute.create(
            {
                "name": "Year",
            }
        )
        cls.attribute_value_2000 = cls.product_attribute_value.create(
            {
                "name": "2000",
                "attribute_id": cls.product_attribute_year.id,
            }
        )
        cls.attribute_value_2001 = cls.product_attribute_value.create(
            {
                "name": "2001",
                "attribute_id": cls.product_attribute_year.id,
            }
        )
        cls.product_wine = cls.product_template.create(
            {
                "name": "Wine",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.product_attribute_year.id,
                            "value_ids": [(4, cls.attribute_value_2000.id)],
                        },
                    ),
                ],
            }
        )
        cls.product_whiskey = cls.product_template.create(
            {
                "name": "Whiskey",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.product_attribute_year.id,
                            "value_ids": [(4, cls.attribute_value_2001.id)],
                        },
                    ),
                ],
            }
        )

    def test_create_new_other_attribute_value(self):
        """
        Testing the new attribute value wasn't added to the products
        if the attribute line auto add is disabled
        """

        attribute_value_2002 = self.product_attribute_value.create(
            {
                "name": "2002",
                "attribute_id": self.product_attribute_year.id,
            }
        )

        wine_attr_line = self.product_wine.attribute_line_ids.filtered(
            lambda line: line.attribute_id == self.product_attribute_year
        )
        whiskey_attr_line = self.product_whiskey.attribute_line_ids.filtered(
            lambda line: line.attribute_id == self.product_attribute_year
        )

        self.assertEqual(
            len(wine_attr_line.value_ids), 1, "Wine attribute line should have 1 value"
        )
        self.assertEqual(
            len(whiskey_attr_line.value_ids),
            1,
            "Whiskey attribute line should have 1 value",
        )
        self.assertNotIn(attribute_value_2002, wine_attr_line.value_ids)
        self.assertNotIn(attribute_value_2002, whiskey_attr_line.value_ids)

    def test_create_new_other_attribute_value_with_auto_add(self):
        """
        Testing the new attribute value was added to the products
        if the attribute line auto add is enabled
        """

        self.product_attribute_year.write(
            {
                "attribute_line_auto_add": True,
            }
        )

        attribute_value_2002 = self.product_attribute_value.create(
            {
                "name": "2002",
                "attribute_id": self.product_attribute_year.id,
            }
        )

        wine_attr_line = self.product_wine.attribute_line_ids.filtered(
            lambda line: line.attribute_id == self.product_attribute_year
        )
        whiskey_attr_line = self.product_whiskey.attribute_line_ids.filtered(
            lambda line: line.attribute_id == self.product_attribute_year
        )

        self.assertEqual(
            len(wine_attr_line.value_ids), 2, "Wine attribute line should have 2 values"
        )
        self.assertEqual(
            len(whiskey_attr_line.value_ids),
            2,
            "Whiskey attribute line should have 2 values",
        )
        self.assertIn(attribute_value_2002, wine_attr_line.value_ids)
        self.assertIn(attribute_value_2002, whiskey_attr_line.value_ids)
