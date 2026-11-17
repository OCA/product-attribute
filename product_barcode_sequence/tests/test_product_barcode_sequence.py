# Copyright 2026 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestProductBarcodeSequence(TransactionCase):
    """Test essential workflows for product barcode sequence module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test category with barcode configuration
        cls.category_electronics = cls.env["product.category"].create(
            {
                "name": "Electronics",
                "auto_generate_barcode": True,
                "barcode_prefix": "123456",
            }
        )

        # Create test category without barcode configuration
        cls.category_general = cls.env["product.category"].create(
            {
                "name": "General",
            }
        )

        # Create existing product with barcode in disabled category to avoid
        # auto-generation
        cls.existing_product = cls.env["product.product"].create(
            {
                "name": "Existing Product",
                "categ_id": cls.category_general.id,
                "barcode": "1234560000018",
            }
        )

    # ==================== HELPER FUNCTIONS ====================

    def _create_category_with_barcode_config(self, name, prefix, auto_generate=True):
        """Helper: Create category with barcode configuration."""
        return self.env["product.category"].create(
            {
                "name": name,
                "auto_generate_barcode": auto_generate,
                "barcode_prefix": prefix,
            }
        )

    def _create_product_in_category(self, name, category, default_code=None):
        """Helper: Create product in specific category."""
        vals = {
            "name": name,
            "categ_id": category.id,
            "default_code": default_code or "",
        }
        return self.env["product.product"].create(vals)

    def _verify_barcode_format(self, barcode, expected_prefix):
        """Helper: Verify barcode has correct EAN-13 format."""
        self.assertEqual(len(barcode), 13, "Barcode must be 13 digits")
        self.assertTrue(barcode.isdigit(), "Barcode must contain only digits")
        self.assertTrue(
            barcode.startswith(expected_prefix),
            f"Barcode must start with prefix {expected_prefix}",
        )

        # Verify GTIN check digit
        barcode_without_check = barcode[:12]
        expected_check_digit = self._calculate_gtin_check_digit(barcode_without_check)
        self.assertEqual(
            int(barcode[-1]), expected_check_digit, "GTIN check digit is incorrect"
        )

    def _calculate_gtin_check_digit(self, barcode_without_check):
        """Helper: Calculate GTIN check digit (same as product method)."""
        odd_sum = sum(int(barcode_without_check[i]) for i in range(0, 12, 2))
        even_sum = sum(int(barcode_without_check[i]) for i in range(1, 12, 2))
        total = odd_sum + (even_sum * 3)
        check_digit = (10 - (total % 10)) % 10
        return check_digit

    def _get_sequence_next_number(self, category):
        """Helper: Get next sequence number for category."""
        return category.barcode_sequence_id.number_next_actual

    # ==================== WORKFLOW TESTS ====================

    def test_workflow_01_category_sequence_creation(self):
        """Workflow: Category sequence creation when setting barcode prefix."""
        # Step 1: Create category without prefix
        category = self._create_category_with_barcode_config("Test Category", "", False)
        self.assertFalse(
            category.barcode_sequence_id, "No sequence should exist without prefix"
        )

        # Step 2: Set barcode prefix
        category.write({"barcode_prefix": "789012"})

        # Step 3: Verify sequence was created
        self.assertTrue(category.barcode_sequence_id, "Sequence should be created")
        self.assertEqual(category.barcode_sequence_id.prefix, "789012")
        self.assertEqual(category.barcode_sequence_id.padding, 6)  # 12 - 6 = 6

    def test_workflow_02_automatic_barcode_generation_on_product_creation(self):
        """Workflow: Automatic barcode generation when creating product."""
        # Step 1: Verify sequence starting point
        initial_seq_num = self._get_sequence_next_number(self.category_electronics)

        # Step 2: Create product in barcode-enabled category
        product = self._create_product_in_category(
            "Test Product", self.category_electronics
        )

        # Step 3: Verify barcode was generated
        self.assertTrue(product.barcode, "Barcode should be generated automatically")
        self._verify_barcode_format(product.barcode, "123456")

        # Step 4: Verify sequence was incremented
        final_seq_num = self._get_sequence_next_number(self.category_electronics)
        self.assertEqual(
            final_seq_num, initial_seq_num + 1, "Sequence should be incremented"
        )

    def test_workflow_03_no_barcode_generation_for_disabled_category(self):
        """Workflow: No barcode generation for category without auto-generate."""
        # Step 1: Create category with prefix but disabled auto-generation
        category = self._create_category_with_barcode_config(
            "Disabled Category", "111111", False
        )

        # Step 2: Create product in disabled category
        product = self._create_product_in_category("Test Product", category)

        # Step 3: Verify no barcode was generated
        self.assertFalse(product.barcode, "No barcode should be generated")
        self.assertFalse(
            product.can_generate_barcode,
            "Product should not be eligible for barcode generation",
        )

    def test_workflow_04_manual_barcode_generation_action(self):
        """Workflow: Manual barcode generation using action."""
        # Step 1: Create product in disabled category first, then move to enabled
        product = self._create_product_in_category(
            "Manual Test Product", self.category_general
        )
        self.assertFalse(product.barcode, "Product should start without barcode")

        # Move to enabled category
        product.write({"categ_id": self.category_electronics.id})
        self.assertFalse(
            product.barcode,
            "Product should still not have barcode after category change",
        )

        # Step 2: Execute manual barcode generation action
        action_result = product.action_generate_barcode()

        # Step 3: Verify barcode was generated
        self.assertTrue(product.barcode, "Barcode should be generated manually")
        self._verify_barcode_format(product.barcode, "123456")

        # Step 4: Verify action returned success notification
        self.assertEqual(action_result["type"], "ir.actions.client")
        self.assertEqual(action_result["tag"], "display_notification")
        self.assertIn("Successfully", action_result["params"]["message"])

    def test_workflow_05_bulk_barcode_generation(self):
        """Workflow: Bulk barcode generation for multiple products."""
        # Step 1: Create multiple products in disabled category first
        products = self.env["product.product"]
        for i in range(3):
            product = self._create_product_in_category(
                f"Bulk Product {i+1}", self.category_general
            )
            products += product
            self.assertFalse(
                product.barcode, f"Product {i+1} should start without barcode"
            )

        # Move all products to enabled category
        products.write({"categ_id": self.category_electronics.id})

        # Verify they still don't have barcodes
        for i, product in enumerate(products):
            self.assertFalse(
                product.barcode,
                f"Product {i+1} should still not have barcode after category change",
            )

        # Step 2: Execute bulk barcode generation
        generated_products = products._generate_barcodes()

        # Step 3: Verify all products got barcodes
        self.assertEqual(len(generated_products), 3, "All products should be generated")
        for product in products:
            self.assertTrue(product.barcode, "Product should have barcode")
            self._verify_barcode_format(product.barcode, "123456")

        # Step 4: Verify barcodes are unique
        barcodes = products.mapped("barcode")
        self.assertEqual(
            len(barcodes), len(set(barcodes)), "All barcodes should be unique"
        )

    def test_workflow_06_category_sequence_update(self):
        """Workflow: Update category barcode prefix and sequence."""
        # Step 1: Create category with initial prefix
        category = self._create_category_with_barcode_config("Update Test", "111111")
        initial_sequence_id = category.barcode_sequence_id.id

        # Step 2: Update prefix
        category.write({"barcode_prefix": "222222"})

        # Step 3: Verify sequence was updated (not recreated)
        self.assertEqual(
            category.barcode_sequence_id.id,
            initial_sequence_id,
            "Same sequence should be updated, not recreated",
        )
        self.assertEqual(
            category.barcode_sequence_id.prefix,
            "222222",
            "Sequence prefix should be updated",
        )
        self.assertEqual(
            category.barcode_sequence_id.padding,
            6,
            "Sequence padding should be updated",
        )

    def test_workflow_07_error_handling_invalid_prefix(self):
        """Workflow: Error handling for invalid barcode prefix."""
        # Step 1: Try to create category with non-digit prefix
        with self.assertRaises(UserError) as context:
            self.env["product.category"].create(
                {
                    "name": "Invalid Category",
                    "auto_generate_barcode": True,
                    "barcode_prefix": "ABC123",
                }
            )

        # Step 2: Verify error message
        self.assertIn("must contain only digits", str(context.exception))

    def test_workflow_08_gtin_check_digit_calculation(self):
        """Workflow: GTIN check digit calculation accuracy."""
        # Step 1: Test known barcode examples
        test_cases = [
            ("123456000001", 2),  # Correct GTIN check digit
            ("123456000002", 9),  # Correct GTIN check digit
            ("123456000003", 6),  # Correct GTIN check digit
        ]

        for barcode_without_check, expected_check_digit in test_cases:
            # Step 2: Calculate check digit
            calculated = self._calculate_gtin_check_digit(barcode_without_check)

            # Step 3: Verify calculation
            self.assertEqual(
                calculated,
                expected_check_digit,
                f"Check digit for {barcode_without_check} should be "
                f"{expected_check_digit}",
            )

    def test_workflow_09_computed_field_can_generate_barcode(self):
        """Workflow: Computed field can_generate_barcode behavior."""
        # Step 1: Test product in enabled category without barcode
        product = self._create_product_in_category(
            "Test Product", self.category_general
        )
        # Move to enabled category but don't generate barcode
        product.write({"categ_id": self.category_electronics.id})
        self.assertTrue(
            product.can_generate_barcode,
            "Product in enabled category without barcode should be generatable",
        )

        # Step 2: Test product with existing barcode (use unique barcode)
        product.write({"barcode": "9999999999999"})
        self.assertFalse(
            product.can_generate_barcode,
            "Product with existing barcode should not be generatable",
        )

        # Step 3: Test product in disabled category
        product.write({"barcode": False, "categ_id": self.category_general.id})
        self.assertFalse(
            product.can_generate_barcode,
            "Product in disabled category should not be generatable",
        )

        # Step 4: Test product in category without sequence
        category_no_seq = self._create_category_with_barcode_config("No Seq", "", True)
        product.write({"categ_id": category_no_seq.id})
        self.assertFalse(
            product.can_generate_barcode,
            "Product in category without sequence should not be generatable",
        )

    def test_workflow_10_force_barcode_regeneration(self):
        """Workflow: Force barcode regeneration for existing barcodes."""
        # Step 1: Create product with existing barcode
        # (in disabled category to avoid auto-generation)
        product = self._create_product_in_category(
            "Force Test Product", self.category_general
        )
        product.write({"barcode": "9999999999999"})
        original_barcode = product.barcode
        self.assertTrue(product.barcode, "Product should start with barcode")

        # Move to enabled category
        product.write({"categ_id": self.category_electronics.id})

        # Step 2: Force regenerate barcode
        generated_products = product._generate_barcodes(force=True)

        # Step 3: Verify barcode was changed
        self.assertNotEqual(
            product.barcode,
            original_barcode,
            "Barcode should be different after force regeneration",
        )
        self._verify_barcode_format(product.barcode, "123456")
        self.assertIn(
            product, generated_products, "Product should be in generated products"
        )

    def test_workflow_11_bidirectional_sync_sequence_to_prefix(self):
        """Workflow: Barcode prefix updates when sequence is set."""
        # Step 1: Create category without prefix
        category = self._create_category_with_barcode_config("Sync Test", "", False)

        # Step 2: Create a sequence manually
        sequence = self.env["ir.sequence"].create(
            {
                "name": "Test Sequence",
                "code": "product.barcode - 333333",
                "prefix": "333333",
                "padding": 6,
                "company_id": False,
            }
        )

        # Step 3: Set the sequence on category
        category.write({"barcode_sequence_id": sequence.id})

        # Step 4: Verify prefix was updated from sequence
        self.assertEqual(category.barcode_prefix, "333333")
        self.assertEqual(category.barcode_sequence_id, sequence)

    def test_workflow_12_sequence_reuse_across_categories(self):
        """Workflow: Multiple categories reuse the same sequence when prefix matches."""
        # Step 1: Create first category with prefix
        category1 = self._create_category_with_barcode_config("Category 1", "444444")
        sequence1_id = category1.barcode_sequence_id.id

        # Step 2: Create second category with same prefix
        category2 = self._create_category_with_barcode_config("Category 2", "444444")

        # Step 3: Verify same sequence is reused
        self.assertEqual(
            category1.barcode_sequence_id.id,
            category2.barcode_sequence_id.id,
            "Same sequence should be reused for same prefix",
        )
        self.assertEqual(sequence1_id, category2.barcode_sequence_id.id)

    def test_workflow_13_clear_barcode_configuration(self):
        """Workflow: Clear barcode prefix and sequence."""
        # Step 1: Create category with barcode configuration
        category = self._create_category_with_barcode_config("Clear Test", "555555")
        self.assertTrue(category.barcode_sequence_id, "Sequence should exist")

        # Step 2: Clear the prefix
        category.write({"barcode_prefix": ""})

        # Step 3: Verify both fields are cleared
        self.assertFalse(category.barcode_prefix, "Prefix should be cleared")
        self.assertFalse(category.barcode_sequence_id, "Sequence should be cleared")
