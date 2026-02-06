"""
Test UC2: Template-First Packaging with Variant Scope Limiting

As a product manager, I want to define packaging at the template level
with optional variant-specific scope limiting so that variants can share
 common packaging while allowing specific overrides.

Acceptance Criteria:
- Every packaging configuration has a product_tmpl_id (required)
- Optionally has product_variant_ids to limit scope to specific variants
- If product_variant_ids is empty → applies to ALL variants of the template
- If product_variant_ids has variants → applies ONLY to those specific variants
- Cannot create duplicate template/UoM/package_type/qty combinations
- All selected variants must belong to the specified product template
"""

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestUC2TemplateFirstPackagingWithVariantScope(TransactionCase):
    """Test UC2: Template-First Packaging with Variant Scope Limiting"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Create attribute and values for variant generation
        cls.attr_size = cls.env["product.attribute"].create({"name": "Size"})
        cls.attr_val_small = cls.env["product.attribute.value"].create(
            {"name": "Small", "attribute_id": cls.attr_size.id}
        )
        cls.attr_val_large = cls.env["product.attribute.value"].create(
            {"name": "Large", "attribute_id": cls.attr_size.id}
        )

        # Create a template with multiple variants
        cls.template = cls.env["product.template"].create(
            {
                "name": "Multi-Variant Product",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [
                                Command.set(
                                    [cls.attr_val_small.id, cls.attr_val_large.id]
                                )
                            ],
                        }
                    )
                ],
            }
        )

        # Get the generated variants
        cls.variants = cls.template.product_variant_ids
        cls.variant_small = cls.variants[0]
        cls.variant_large = cls.variants[1]

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

    @mute_logger("odoo.sql_db")
    def test_packaging_configuration_requires_template(self):
        """UC2: Every packaging configuration has a product_tmpl_id (required)."""
        with self.assertRaises(IntegrityError):
            self.ProductUomPackaging.create(
                {
                    "uom_id": self.uom_dozen.id,
                    "package_type_id": self.package_small.id,
                }
            )

    def test_empty_variant_ids_applies_to_all_variants(self):
        """UC2: Empty product_variant_ids means packaging applies to all variants."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertFalse(packaging.product_variant_ids)

    def test_non_empty_variant_ids_limits_scope(self):
        """UC2: Non-empty product_variant_ids limits scope to those variants."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "product_variant_ids": [Command.set([self.variant_small.id])],
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(packaging.product_variant_ids, self.variant_small)

    def test_variants_must_belong_to_template(self):
        """UC2: All selected variants must belong to the specified product template."""
        other_template = self.env["product.template"].create({"name": "Other Product"})
        other_variant = other_template.product_variant_ids[0]

        with self.assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.template.id,
                    "product_variant_ids": [Command.set([other_variant.id])],
                    "uom_id": self.uom_unit.id,
                    "package_type_id": self.package_small.id,
                }
            )

    def test_duplicate_template_uom_package_type_qty_rejected(self):
        """UC2: Cannot create duplicate template/UoM/package_type/qty combinations."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
                "qty": 12.0,
            }
        )
        with self.assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.template.id,
                    "uom_id": self.uom_dozen.id,
                    "package_type_id": self.package_small.id,
                    "qty": 12.0,
                }
            )

    def test_template_and_variant_specific_can_coexist(self):
        """UC2: Template-level and variant-specific packaging can coexist."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
                "name": "Small Box (Dozen)",
            }
        )
        variant_packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "product_variant_ids": [Command.set([self.variant_small.id])],
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "name": "Small Box (Unit)",
            }
        )
        self.assertTrue(variant_packaging.product_variant_ids)

    def test_multiple_variants_in_single_packaging(self):
        """UC2: Single packaging can apply to multiple variants."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.template.id,
                "product_variant_ids": [
                    Command.set([self.variant_small.id, self.variant_large.id])
                ],
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(len(packaging.product_variant_ids), 2)
