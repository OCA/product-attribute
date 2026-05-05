# Copyright 2026 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import Form

from .common import ProductSetCommon


class TestProductSetLine(ProductSetCommon):
    """Tests for product.set.line uom_id field."""

    def test_product_uom_id_false_without_product(self):
        """uom_id is False for section/note lines that have no product."""
        line = self.env["product.set.line"].create(
            {
                "product_set_id": self.product_set_1.id,
                "display_type": "line_section",
                "name": "Test Section",
                "quantity": 1,
            }
        )
        self.assertFalse(line.product_uom_id)

    def test_product_uom_id_can_be_manually_overridden(self):
        """uom_id accepts a manual value different from the product default."""
        uom_unit = self.env.ref("uom.product_uom_unit")
        product_uom_unit = self.env["product.uom"].create(
            {
                "barcode": "Unit Dozen",
                "uom_id": uom_unit.id,
                "product_id": self.product.id,
            }
        )
        self.product_set_line_1.product_uom_id = product_uom_unit
        self.assertEqual(self.product_set_line_1.product_uom_id, product_uom_unit)

    def test_product_uom_id_recomputes_on_product_change(self):
        """uom_id is recomputed when product_id changes to reflect the new product's
        UOM."""
        other_product = self.env["product.product"].create({"name": "Other Product"})
        self.product_set_line_1.product_id = other_product
        self.assertEqual(
            self.product_set_line_1.product_uom_id.uom_id, other_product.uom_id
        )

    def test_product_uom_id_cleared_when_product_removed(self):
        # uom_id becomes False when the product is unset via onchange (form simulation).
        self.env.user.group_ids |= self.env.ref("uom.group_uom")
        with Form(self.product_set_1) as set_form:
            with set_form.set_line_ids.edit(0) as line_form:
                self.assertTrue(line_form.product_uom_id)
                line_form.product_id = self.env["product.product"]
                self.assertFalse(line_form.product_uom_id)
                line_form.product_id = self.product

    def test_product_uom_id_stored_on_create(self):
        """uom_id is stored in the database immediately on creation."""
        line = self.env["product.set.line"].create(
            {
                "product_set_id": self.product_set_1.id,
                "product_id": self.product.id,
                "quantity": 3,
                "product_uom_id": self.product_uom_1.id,
            }
        )
        # Invalidate cache to force a DB read
        line.invalidate_recordset(["product_uom_id"])
        self.assertEqual(line.product_uom_id, self.product_uom_1)

    def test_set_with_multiple_lines_uom(self):
        """A product set with multiple lines each carry the correct UOM."""
        uom_unit = self.env.ref("uom.product_uom_unit")
        uom_meter = self.env.ref("uom.product_uom_meter")
        uom_cm = self.env.ref("uom.product_uom_cm")

        product_uom_cm = self.env["product.uom"].create(
            {
                "barcode": "Centimeter",
                "uom_id": uom_cm.id,
                "product_id": self.product.id,
            }
        )
        product_a = self.env["product.product"].create(
            {"name": "Product A", "uom_id": uom_unit.id}
        )
        product_b = self.env["product.product"].create(
            {"name": "Product B", "uom_id": uom_meter.id}
        )
        prod_set = self.env["product.set"].create(
            {
                "name": "Multi UOM Set",
                "set_line_ids": [
                    Command.create({"product_id": product_a.id, "quantity": 1}),
                    Command.create(
                        {
                            "product_id": product_b.id,
                            "quantity": 2,
                            "product_uom_id": product_uom_cm.id,
                        }
                    ),
                ],
            }
        )
        line_a, line_b = prod_set.set_line_ids
        self.assertFalse(line_a.product_uom_id)
        self.assertEqual(line_b.product_uom_id.uom_id, uom_cm)
