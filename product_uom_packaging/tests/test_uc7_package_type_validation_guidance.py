"""
Test UC7: Package Type Validation Guidance

As a warehouse manager, I want to receive warnings when package types seem inappropriate
so that we avoid packaging mistakes.

Acceptance Criteria:
- Warning when product weight exceeds package type's max_weight
- Warning when product volume seems incompatible with package dimensions
- Warnings are informational (don't block operations)
- Validation considers product weight + package base weight
- Volume calculation: length × width × height of package type
"""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


class TestUC7PackageTypeValidationGuidance(TransactionCase):
    """Test UC7: Package Type Validation Guidance"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Products
        cls.product_a = cls.env["product.product"].create({"name": "Product A"})

        # UoMs
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")

        # Package Types
        cls.package_small = cls.env["stock.package.type"].create(
            {
                "name": "Small Box",
                "packaging_length": 10,
                "width": 10,
                "height": 10,
                "base_weight": 0.5,
                "max_weight": 10,
            }
        )

    def test_weight_validation_warning(self):
        """UC7: Warning when product weight exceeds package type's max_weight."""
        light_package = self.env["stock.package.type"].create(
            {
                "name": "Light Package",
                "max_weight": 5.0,
            }
        )

        heavy_product = self.env["product.product"].create(
            {
                "name": "Heavy Product",
                "weight": 10.0,
            }
        )

        move_line = self.env["stock.move.line"].create(
            {
                "product_id": heavy_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": light_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertTrue(
            hasattr(move_line, "package_compatibility_warning"),
            "stock.move.line should have package_compatibility_warning field",
        )

        warning_message = move_line.package_compatibility_warning
        self.assertIsNotNone(
            warning_message, "Warning should be generated for weight incompatibility"
        )
        self.assertIn(
            "weight", warning_message.lower(), "Warning message should mention weight"
        )
        self.assertIn(
            "10.0", warning_message, "Warning should show actual product weight"
        )
        self.assertIn("5.0", warning_message, "Warning should show package max weight")

        self.assertTrue(
            hasattr(move_line, "is_package_incompatible"),
            "stock.move.line should have is_package_incompatible field",
        )
        self.assertTrue(
            move_line.is_package_incompatible,
            "Incompatible flag should be True for weight issues",
        )

        # Test compatible case (no warning)
        compatible_move_line = self.env["stock.move.line"].create(
            {
                "product_id": self.product_a.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": light_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertFalse(
            compatible_move_line.is_package_incompatible,
            "Compatible flag should be False for valid weight",
        )
        self.assertFalse(
            compatible_move_line.package_compatibility_warning,
            "No warning should be generated for compatible weight",
        )

    def test_weight_validation_multiple_quantities(self):
        """UC7: Warning when multiple product quantities exceed max_weight."""
        medium_package = self.env["stock.package.type"].create(
            {
                "name": "Medium Package",
                "max_weight": 7.0,
            }
        )

        medium_product = self.env["product.product"].create(
            {
                "name": "Medium Product",
                "weight": 5.0,
            }
        )

        # 1 qty (5 lbs) should be compatible with 7 lbs package
        compatible_move_line = self.env["stock.move.line"].create(
            {
                "product_id": medium_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": medium_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertFalse(
            compatible_move_line.is_package_incompatible,
            "Single 5 lb item should be compatible with 7 lb package",
        )
        self.assertFalse(
            compatible_move_line.package_compatibility_warning,
            "No warning should be generated for compatible weight",
        )

        # 2 qty (10 lbs) should be incompatible with 7 lbs package
        incompatible_move_line = self.env["stock.move.line"].create(
            {
                "product_id": medium_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 2.0,
                "package_type_id": medium_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertTrue(
            incompatible_move_line.is_package_incompatible,
            "Two 5 lb items should be incompatible with 7 lb package",
        )
        self.assertIn(
            "Weight incompatibility",
            incompatible_move_line.package_compatibility_warning,
        )
        self.assertIn(
            "10.0",
            incompatible_move_line.package_compatibility_warning,
        )
        self.assertIn(
            "7.0",
            incompatible_move_line.package_compatibility_warning,
        )

        # Edge case: exactly at limit (10 lb package)
        large_package = self.env["stock.package.type"].create(
            {
                "name": "Large Package",
                "max_weight": 10.0,
            }
        )

        edge_case_move_line = self.env["stock.move.line"].create(
            {
                "product_id": medium_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 2.0,
                "package_type_id": large_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertFalse(
            edge_case_move_line.is_package_incompatible,
            "Weight exactly at package limit should be compatible",
        )
        self.assertFalse(
            edge_case_move_line.package_compatibility_warning,
            "No warning should be generated at exact limit",
        )

    def test_volume_incompatibility_warning(self):
        """UC7: Warning when product volume exceeds package volume."""
        # Package with dimensions but no weight limit (max_weight=0 means no limit)
        small_package = self.env["stock.package.type"].create(
            {
                "name": "Tiny Package",
                "packaging_length": 2,
                "width": 2,
                "height": 2,
                "max_weight": 0,
            }
        )

        bulky_product = self.env["product.product"].create(
            {
                "name": "Bulky Product",
                "volume": 100.0,
            }
        )

        move_line = self.env["stock.move.line"].create(
            {
                "product_id": bulky_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": small_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertTrue(
            move_line.is_package_incompatible,
            "Volume exceeding package should be incompatible",
        )
        self.assertIn(
            "Volume incompatibility",
            move_line.package_compatibility_warning,
        )
        self.assertIn("100.0", move_line.package_compatibility_warning)
        self.assertIn("8.0", move_line.package_compatibility_warning)

    def test_picking_no_incompatibility_warning(self):
        """UC7: Picking with compatible move lines shows no warning."""
        compatible_package = self.env["stock.package.type"].create(
            {
                "name": "Compatible Package",
                "max_weight": 100.0,
            }
        )

        light_product = self.env["product.product"].create(
            {
                "name": "Light Product",
                "weight": 1.0,
            }
        )

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "partner_id": self.env["res.partner"]
                .create({"name": "Test Customer"})
                .id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_id": light_product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.uom_unit.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
            }
        )

        picking.action_confirm()
        picking.action_assign()

        move_line = picking.move_line_ids[0]
        move_line.package_type_id = compatible_package

        self.assertFalse(
            picking.has_package_incompatibility,
            "Compatible picking should have no incompatibility flag",
        )
        self.assertFalse(
            picking.package_incompatibility_warning,
            "Compatible picking should have no warning",
        )

    def test_picking_mixed_compatible_and_incompatible(self):
        """UC7: Picking with mix of compatible and incompatible lines."""
        light_package = self.env["stock.package.type"].create(
            {
                "name": "Light Package",
                "max_weight": 5.0,
            }
        )

        heavy_product = self.env["product.product"].create(
            {
                "name": "Heavy Product",
                "weight": 10.0,
            }
        )
        light_product = self.env["product.product"].create(
            {
                "name": "Light Product",
                "weight": 1.0,
            }
        )

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "partner_id": self.env["res.partner"]
                .create({"name": "Test Customer"})
                .id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        for product in [heavy_product, light_product]:
            self.env["stock.move"].create(
                {
                    "picking_id": picking.id,
                    "product_id": product.id,
                    "product_uom_qty": 1.0,
                    "product_uom": self.uom_unit.id,
                    "location_id": picking.location_id.id,
                    "location_dest_id": picking.location_dest_id.id,
                }
            )

        picking.action_confirm()
        picking.action_assign()

        for line in picking.move_line_ids:
            line.package_type_id = light_package

        self.assertTrue(
            picking.has_package_incompatibility,
            "Picking with at least one incompatible line should flag",
        )
        self.assertIn(
            "Heavy Product",
            picking.package_incompatibility_warning,
        )

    def test_no_warning_when_volume_fits(self):
        """UC7: No volume warning when product volume fits in package."""
        big_package = self.env["stock.package.type"].create(
            {
                "name": "Big Package",
                "packaging_length": 10,
                "width": 10,
                "height": 10,
                "max_weight": 0,
            }
        )

        small_product = self.env["product.product"].create(
            {
                "name": "Small Product",
                "volume": 5.0,
            }
        )

        move_line = self.env["stock.move.line"].create(
            {
                "product_id": small_product.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": big_package.id,
                "company_id": self.env.user.company_id.id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.assertFalse(
            move_line.is_package_incompatible,
            "Product volume fitting in package should be compatible",
        )
        self.assertFalse(
            move_line.package_compatibility_warning,
            "No warning when volume fits",
        )


@tagged("-at_install", "post_install")
class TestPackageWarningUI(HttpCase):
    """UC7: Browser tour tests for package compatibility warning UI display."""

    def test_package_warning_ui_display(self):
        """UC7: Package compatibility warnings are displayed in the UI."""
        light_package = self.env["stock.package.type"].create(
            {
                "name": "Light Package",
                "max_weight": 5.0,
            }
        )

        heavy_product = self.env["product.product"].create(
            {
                "name": "Heavy Product",
                "weight": 10.0,
            }
        )

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "partner_id": self.env["res.partner"]
                .create({"name": "Test Customer"})
                .id,
                "location_id": 1,
                "location_dest_id": 2,
            }
        )

        self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_id": heavy_product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.env.ref("uom.product_uom_unit").id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
            }
        )

        picking.action_confirm()
        picking.action_assign()

        move_line = picking.move_line_ids[0]
        move_line.package_type_id = light_package

        tour_url = f"/odoo/stock.picking/{picking.id}"
        self.start_tour(
            tour_url, "test_package_warning_ui_display", login="admin", timeout=15
        )
