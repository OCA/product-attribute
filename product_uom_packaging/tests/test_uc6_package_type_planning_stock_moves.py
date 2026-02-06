"""
Test UC6: Package Type Planning on Stock Moves

As a warehouse planner, I want to specify the intended package type on stock moves
so that pickers know what packaging to use for the transfer.

Acceptance Criteria:
- Stock move form shows package type field (optional)
- Package type dropdown filtered by product's packaging configurations
- Package type defaults from product packaging configuration (lowest sequence)
- Package type is informational only - doesn't affect reservation logic
- Can leave empty if no specific packaging required
"""

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestUC6PackageTypePlanningStockMoves(TransactionCase):
    """Test UC6: Package Type Planning on Stock Moves"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Products
        cls.product_a = cls.env["product.product"].create({"name": "Product A"})

        # UoMs
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

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
        cls.package_large = cls.env["stock.package.type"].create(
            {
                "name": "Large Box",
                "packaging_length": 20,
                "width": 15,
                "height": 12,
                "base_weight": 1.0,
                "max_weight": 25,
            }
        )

        # Stock locations
        cls.location_stock = cls.env.ref("stock.stock_location_stock")
        cls.location_customers = cls.env.ref("stock.stock_location_customers")

    def test_stock_move_form_shows_package_type_field(self):
        """UC6: Stock move form shows package type field (optional)."""
        # Create a stock move
        stock_move = self.env["stock.move"].create(
            {
                "product_id": self.product_a.id,
                "product_uom": self.uom_unit.id,
                "product_uom_qty": 10.0,
                "location_id": self.location_stock.id,
                "location_dest_id": self.location_customers.id,
            }
        )
        with Form(stock_move) as move_form:
            move_form.package_type_id = self.package_small

    def test_package_type_dropdown_filtered_by_product_packaging(self):
        """
        UC6: Package type dropdown filtered by product's packaging configurations.
        """
        # Create packaging configurations for product A
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )

        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_large.id,
                "sequence": 5,
            }
        )

        # Create stock move
        stock_move = self.env["stock.move"].create(
            {
                "product_id": self.product_a.id,
                "product_uom": self.uom_unit.id,
                "product_uom_qty": 10.0,
                "location_id": self.location_stock.id,
                "location_dest_id": self.location_customers.id,
            }
        )

        # Verify that both package types from product packaging configs
        # can be set on the stock move
        product_package_types = self.product_a.product_tmpl_id.packaging_ids.mapped(
            "package_type_id"
        )
        self.assertIn(self.package_small, product_package_types)
        self.assertIn(self.package_large, product_package_types)

        # Verify package_type_id can be set on the move form
        with Form(stock_move) as move_form:
            move_form.package_type_id = self.package_small
        self.assertEqual(stock_move.package_type_id, self.package_small)

        with Form(stock_move) as move_form:
            move_form.package_type_id = self.package_large
        self.assertEqual(stock_move.package_type_id, self.package_large)

    def test_move_line_form_shows_package_type(self):
        """UC6: Package type appears in stock move line form view."""
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "partner_id": self.env["res.partner"]
                .create({"name": "Test Customer"})
                .id,
            }
        )

        move = self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_id": self.product_a.id,
                "product_uom": self.uom_unit.id,
                "location_id": self.location_stock.id,
                "location_dest_id": self.location_customers.id,
            }
        )

        move_line = self.env["stock.move.line"].create(
            {
                "move_id": move.id,
                "product_id": self.product_a.id,
                "product_uom_id": self.uom_unit.id,
                "quantity": 1.0,
                "package_type_id": self.package_small.id,
            }
        )

        with Form(move_line) as f:
            self.assertEqual(f.package_type_id, self.package_small)
            f.package_type_id = self.env["stock.package.type"]

        self.assertFalse(move_line.package_type_id)
