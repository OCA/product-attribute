"""
Test UC1: Define Product-Specific Package Dimensions

As a warehouse manager, I want to specify which package type
(with dimensions) applies to a product in a given UoM
so that shipping costs and storage planning are accurate.

Acceptance Criteria:
- Can create a link between product, UoM, and package type
- Quantity defaults to 1.0
- Same product/UoM/package_type with different qty is allowed (e.g. half/full pallet)
- Duplicate product/UoM/package_type/qty is rejected
- Name defaults to package type name, is user-editable, unique per product/company
"""

from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestUC1DefineProductSpecificPackageDimensions(TransactionCase):
    """Test UC1: Define Product-Specific Package Dimensions"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Products
        cls.product_bricks = cls.env["product.product"].create({"name": "Bricks"})
        cls.product_soda = cls.env["product.product"].create({"name": "Soda Cans"})

        # UoMs
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        # Package Types with different dimensions
        cls.package_box_12x12x12 = cls.env["stock.package.type"].create(
            {
                "name": "12x12x12 Box",
                "packaging_length": 12,
                "width": 12,
                "height": 12,
                "base_weight": 0.8,
                "max_weight": 15,
            }
        )
        cls.package_box_6x12x8 = cls.env["stock.package.type"].create(
            {
                "name": "6x12x8 Box",
                "packaging_length": 6,
                "width": 12,
                "height": 8,
                "base_weight": 0.3,
                "max_weight": 8,
            }
        )

    def test_quantity_defaults_to_one(self):
        """UC1: Quantity field defaults to 1.0."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_6x12x8.id,
            }
        )
        self.assertEqual(packaging.qty, 1.0)

    def test_same_package_type_different_quantities(self):
        """UC1: Same product/UoM/package_type with different qty is allowed.

        E.g. "Half-Pallet" (16 bricks) and "Full-Pallet" (32 bricks)
        both use the same pallet type.
        """
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_12x12x12.id,
                "qty": 16.0,
                "name": "Half Pallet",
            }
        )
        full_pallet = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_12x12x12.id,
                "qty": 32.0,
                "name": "Full Pallet",
            }
        )
        self.assertTrue(full_pallet.exists())

    @mute_logger("odoo.sql_db")
    def test_cannot_duplicate_product_uom_package_type_qty(self):
        """UC1: Cannot create duplicate product/UoM/package_type/qty combination."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_box_12x12x12.id,
                "qty": 12.0,
            }
        )
        with self._assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                    "uom_id": self.uom_dozen.id,
                    "package_type_id": self.package_box_12x12x12.id,
                    "qty": 12.0,
                }
            )

    def test_name_defaults_to_package_type_name(self):
        """UC1: Name defaults to the package type's name."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_box_12x12x12.id,
            }
        )
        self.assertEqual(packaging.name, self.package_box_12x12x12.name)

    def test_name_is_user_editable(self):
        """UC1: Name can be overridden by the user via the form view."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_12x12x12.id,
            }
        )
        with Form(packaging) as f:
            f.name = "Full Pallet"
        self.assertEqual(packaging.name, "Full Pallet")

    @mute_logger("odoo.sql_db")
    def test_name_unique_per_product_company(self):
        """UC1: Cannot have duplicate names for the same product/company."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_12x12x12.id,
                "name": "Full Pallet",
                "qty": 32.0,
            }
        )
        with self._assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                    "uom_id": self.uom_unit.id,
                    "package_type_id": self.package_box_12x12x12.id,
                    "name": "Full Pallet",
                    "qty": 16.0,
                }
            )

    @mute_logger("odoo.sql_db")
    def test_cannot_duplicate_config_even_with_different_names(self):
        """UC1: Duplicate product/UoM/package_type/qty/company rejected even
        when names differ."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_box_12x12x12.id,
                "qty": 10.0,
                "name": "Name A",
            }
        )
        with self._assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_bricks.product_tmpl_id.id,
                    "uom_id": self.uom_unit.id,
                    "package_type_id": self.package_box_12x12x12.id,
                    "qty": 10.0,
                    "name": "Name B",
                }
            )
