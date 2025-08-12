# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.errors import UniqueViolation

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestProductMerge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test products
        cls.product_r = cls.env["product.template"].create(
            {"name": "Product: Color RED"}
        )
        cls.product_b = cls.env["product.template"].create(
            {"name": "Product: Color Blue"}
        )

        # Create test attributes
        cls.color_attr = cls.env["product.attribute"].create(
            {"name": "Color", "create_variant": "dynamic"}
        )
        cls.color_attr_value_r = cls.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": cls.color_attr.id}
        )
        cls.color_attr_value_b = cls.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": cls.color_attr.id}
        )
        cls.variant_r = cls.product_r.product_variant_ids
        cls.variant_b = cls.product_b.product_variant_ids
        cls.existing_variants = cls.variant_r | cls.variant_b
        cls.supplierinfo_r = cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.env["res.partner"].create({"name": "Supplier A"}).id,
                "product_tmpl_id": cls.product_r.id,
            }
        )
        cls.supplierinfo_b = cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.env["res.partner"].create({"name": "Supplier B"}).id,
                "product_tmpl_id": cls.product_b.id,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.product_r.id,
                            "fixed_price": 70.0,
                        }
                    ),
                    Command.create(
                        {
                            "applied_on": "1_product",
                            "product_tmpl_id": cls.product_b.id,
                            "fixed_price": 50.0,
                        }
                    ),
                ],
            }
        )

    def test_0(self):
        """
        Test the default_get method of the product merge wizard.

        This test validates that:
        - `product_ids` is correctly populated from the context.
        - `line_ids` is computed correctly based on the selected products.
        - Attribute values are assigned correctly to the wizard lines.
        """
        with Form(
            self.env["product.merge.wizard"].with_context(
                active_model="product.template",
                active_ids=[self.product_r.id, self.product_b.id],
            )
        ) as wizard_form:
            wizard_form.product_tmpl_id = self.product_r
        wizard = wizard_form.save()
        self.assertEqual(wizard.product_ids, self.product_r | self.product_b)
        self.assertEqual(len(wizard.line_ids), 2)
        self.assertEqual(wizard.line_ids.product_id, self.existing_variants)
        line_r = wizard.line_ids.filtered(
            lambda line: line.product_id == self.variant_r
        )
        line_b = wizard.line_ids.filtered(
            lambda line: line.product_id == self.variant_b
        )
        line_r.attribute_value_ids = self.color_attr_value_r
        line_b.attribute_value_ids = self.color_attr_value_b
        self.wizard = wizard
        self.line_r = line_r
        self.line_b = line_b
        self.wizard.attribute_ids = self.color_attr
        self.line_r.attribute_value_ids = self.color_attr_value_r
        self.line_b.attribute_value_ids = self.color_attr_value_b

    def test_action_merge_products(self):
        """
        Test the `action_merge_products` method of the wizard:
        - The primary product template remains active after the merge.
        - The other product template is deactivated.
        - The attributes and variants are correctly merged without creating duplicates.
        - Variants are assigned the correct attribute values after the merge.
        """
        self.test_0()
        # Execute the merge
        self.wizard.action_merge_products()

        # Check that product_tmpl_id retains active status
        self.assertTrue(self.product_r.active)

        # Check that other products are archived
        self.assertFalse(self.product_b.active)

        # Check that attributes are updated in product_tmpl_id
        attribute_lines = self.product_r.attribute_line_ids
        self.assertEqual(len(attribute_lines), 1)
        variants = self.product_r.product_variant_ids
        # check variants are now related to on template
        self.assertEqual(len(variants), 2)
        # check variants are the same and the system didn't create new one
        self.assertEqual(self.existing_variants, variants)
        # check values are assigned to variants according to the mapping
        variant_r_tmpl_value = self.variant_r.product_template_attribute_value_ids
        variant_b_tmpl_value = self.variant_b.product_template_attribute_value_ids
        self.assertEqual(
            variant_r_tmpl_value.product_attribute_value_id, self.color_attr_value_r
        )
        self.assertEqual(
            variant_b_tmpl_value.product_attribute_value_id, self.color_attr_value_b
        )

    def test_action_merge_products_same_attribute_value(self):
        """
        ensures that an error is raised when two variants are merged with the same
        attribute value combination
        """
        self.test_0()
        self.wizard.attribute_ids = self.color_attr
        self.line_b.attribute_value_ids = self.color_attr_value_r
        # Execute the merge
        with self.assertRaises(UniqueViolation, msg="Combination exists"):
            self.wizard.action_merge_products()

    def test_minimum_two_products_constraint(self):
        wizard = self.env["product.merge.wizard"].create(
            {
                "product_tmpl_id": self.product_r.id,
                "product_ids": [Command.link(self.product_r.id)],
            }
        )
        with self.assertRaises(
            ValidationError,
            msg="At least two products must be added to the wizard to perform a merge.",
        ):
            wizard.action_merge_products()

    def test_products_with_max_one_variant(self):
        # Create a product template with multiple variants
        self.color_attr.create_variant = "always"
        product_multi_variant = self.env["product.template"].create(
            {
                "name": "Product with Multiple Variants",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color_attr.id,
                            "value_ids": [
                                Command.set(
                                    [
                                        self.color_attr_value_r.id,
                                        self.color_attr_value_b.id,
                                    ],
                                )
                            ],
                        },
                    )
                ],
            }
        )

        # Attempt to create a wizard with a multi-variant product
        wizard = self.env["product.merge.wizard"].create(
            {
                "product_tmpl_id": self.product_r.id,
                "product_ids": [
                    Command.link(self.product_r.id),
                    Command.link(product_multi_variant.id),
                ],
            }
        )
        with self.assertRaises(
            ValidationError, msg="All added products must have at most one variant."
        ):
            wizard.action_merge_products()

    def test_update_supplier_info(self):
        """
        Test the `_update_supplier_info` method:
        - Ensures that supplier information is correctly updated when products are
          merged.
        - Checks that the supplierinfo records are transferred from the merged product
          templates to the target product template and variant.
        """
        self.test_0()
        self.wizard.action_merge_products()

        # Check supplierinfo for product_r
        updated_supplierinfo_r = self.env["product.supplierinfo"].search(
            [("product_id", "=", self.variant_r.id)]
        )
        self.assertEqual(updated_supplierinfo_r, self.supplierinfo_r)
        self.assertEqual(updated_supplierinfo_r.product_tmpl_id, self.product_r)
        updated_supplierinfo_b = self.env["product.supplierinfo"].search(
            [("product_id", "=", self.variant_b.id)]
        )
        self.assertEqual(updated_supplierinfo_b, self.supplierinfo_b)
        self.assertEqual(updated_supplierinfo_b.product_tmpl_id, self.product_r)
        self.assertEqual(len(self.product_r.seller_ids), 2)

    def test_different_type_merge(self):
        """
        Test that merging products of different types raises a ValidationError.
        """
        self.product_r.type = "service"
        with self.assertRaises(ValidationError):
            self.test_0()

    def test_update_price_list(self):
        self.test_0()
        self.wizard.action_merge_products()
        self.assertEqual(self.pricelist.item_ids.product_tmpl_id, self.product_r)
        self.assertEqual(self.pricelist.item_ids[0].applied_on, "0_product_variant")
        self.assertEqual(
            self.pricelist.item_ids.product_id, self.variant_r | self.variant_b
        )
