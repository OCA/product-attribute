# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestProductCode(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_model = cls.env["product.product"]
        cls.template_model = cls.env["product.template"]
        cls.product = cls.product_model.create({"name": "Test Product Code"})

    def test_product_code(self):
        """Check Product Code"""
        self.assertTrue(self.product.default_code, "Product code is not set.")

    def test_product_code_with_provided_code(self):
        """Check that provided default_code is respected"""
        custom_code = "CUSTOM-CODE-123"
        product = self.product_model.create(
            {"name": "Test Product with Custom Code", "default_code": custom_code}
        )
        # Provided code should be respected
        self.assertEqual(
            product.default_code,
            custom_code,
            "Product code should respect the provided default_code.",
        )

    def test_product_code_auto_generated(self):
        """Check that default_code is auto-generated when not provided"""
        product = self.product_model.create({"name": "Test Product without Code"})
        self.assertTrue(product.default_code, "Product code should be auto-generated.")
        self.assertNotEqual(
            product.default_code,
            "",
            "Auto-generated product code should not be empty.",
        )

    def test_template_with_provided_code(self):
        """Check that product.template respects provided default_code"""
        custom_code = "TEMPLATE-CODE-456"
        template = self.template_model.create(
            {"name": "Test Template with Custom Code", "default_code": custom_code}
        )
        # Template variant should have the same code
        self.assertEqual(
            template.product_variant_id.default_code,
            custom_code,
            "Template variant should respect the provided default_code.",
        )

    def test_template_auto_generated_code(self):
        """Check that product.template auto-generates code when not provided"""
        template = self.template_model.create({"name": "Test Template without Code"})
        # Template variant should have an auto-generated code
        self.assertTrue(
            template.product_variant_id.default_code,
            "Template variant should have auto-generated code.",
        )
        self.assertNotEqual(
            template.product_variant_id.default_code,
            "",
            "Auto-generated code should not be empty.",
        )

    def test_empty_string_default_code(self):
        """Check that empty string is treated as no code provided"""
        product = self.product_model.create(
            {"name": "Test Product Empty String", "default_code": ""}
        )
        # Empty string should trigger auto-generation
        self.assertTrue(
            product.default_code, "Empty string should trigger code generation."
        )
        self.assertNotEqual(
            product.default_code,
            "",
            "Auto-generated code should not be empty.",
        )

    def test_template_empty_string_default_code(self):
        """Check that template with empty string default_code auto-generates"""
        template = self.template_model.create(
            {"name": "Test Template Empty String", "default_code": ""}
        )
        # Empty string should trigger auto-generation for variant
        self.assertTrue(
            template.product_variant_id.default_code,
            "Empty string should trigger code generation for template variant.",
        )
        self.assertNotEqual(
            template.product_variant_id.default_code,
            "",
            "Auto-generated code should not be empty.",
        )

    def test_multi_variant_template(self):
        """Check that multi-variant templates handle codes correctly"""
        # Create attribute and values
        attribute = self.env["product.attribute"].create({"name": "Test Attribute"})
        value1 = self.env["product.attribute.value"].create(
            {"name": "Value 1", "attribute_id": attribute.id}
        )
        value2 = self.env["product.attribute.value"].create(
            {"name": "Value 2", "attribute_id": attribute.id}
        )

        # Create template with attributes (multi-variant)
        template = self.template_model.create(
            {
                "name": "Multi-Variant Product",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, [value1.id, value2.id])],
                        },
                    )
                ],
            }
        )

        # Each variant should have its own unique auto-generated code
        variants = template.product_variant_ids
        self.assertEqual(len(variants), 2, "Should have 2 variants")
        codes = variants.mapped("default_code")
        self.assertEqual(len(codes), 2, "Should have 2 codes")
        self.assertEqual(len(set(codes)), 2, "Codes should be unique (no duplicates)")
        # All codes should be non-empty
        for code in codes:
            self.assertTrue(code, "Each variant should have a code")

    def test_multi_variant_template_with_provided_code(self):
        """Check that multi-variant template ignores provided default_code.
        When a template has variants (attribute_line_ids), each variant should
        get its own auto-generated code, even if the template has a default_code.
        """
        # Create attribute and values
        attribute = self.env["product.attribute"].create(
            {"name": "Test Attribute Color"}
        )
        value1 = self.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": attribute.id}
        )
        value2 = self.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": attribute.id}
        )

        # Create multi-variant template WITH a provided default_code
        template_code = "TEMPLATE-MULTI-001"
        template = self.template_model.create(
            {
                "name": "Multi-Variant Product with Code",
                "default_code": template_code,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, [value1.id, value2.id])],
                        },
                    )
                ],
            }
        )

        # Variants should NOT use the template's code
        variants = template.product_variant_ids
        self.assertEqual(len(variants), 2, "Should have 2 variants")

        # Each variant should have a unique auto-generated code
        # NOT the template's provided code
        for variant in variants:
            self.assertNotEqual(
                variant.default_code,
                template_code,
                "Variant should not use template's provided code",
            )
            self.assertTrue(
                variant.default_code.startswith("DEFAULT-"),
                "Variant should have auto-generated code",
            )

        # Codes should be unique
        codes = variants.mapped("default_code")
        self.assertEqual(len(set(codes)), 2, "Each variant should have unique code")

    def test_product_sequence_compatibility(self):
        """Check that codes from other modules (product_sequence) are respected"""
        # Simulate product_sequence creating a product with PROD prefix
        product = self.product_model.create(
            {"name": "Test Product Sequence", "default_code": "PROD0001"}
        )
        # Should respect PROD prefix (from product_sequence)
        self.assertEqual(
            product.default_code,
            "PROD0001",
            "Should respect codes with PROD prefix from other modules.",
        )

        # SEQ prefix should also be respected
        product2 = self.product_model.create(
            {"name": "Test Sequence", "default_code": "SEQ123"}
        )
        self.assertEqual(product2.default_code, "SEQ123", "Should respect SEQ prefix.")
