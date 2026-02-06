"""
Test UC1: Product-Specific Cross-Category Conversion Factor

As a product manager, I want to define a conversion factor on a product's
packaging UoM so that the system can correctly convert between UoMs of
different categories (e.g. volume to weight) for that specific product.

Acceptance Criteria:
- A factor field exists on product.uom.factor and defaults to 1.0
- The factor can store a custom value (e.g. 1.05 for specific gravity)
- The factor represents: 1 unit of the packaging UoM = factor units of the
  product's base UoM (e.g. 1 mL = 1.05 g for ink with SG 1.05)
- The factor for units within the same category cannot be set to a value
  different from the unit's default
- A product.uom.factor record is linked to a product.template via
  product_tmpl_id, with an optional product_ids M2M to restrict to
  specific variants (empty = applies to all variants)
- A variant can only appear on one product.uom.factor per uom_id
- All product_ids must belong to the same product_tmpl_id
- When a cross-category UoM is added to a product's uom_ids, a
  product.uom.factor record is auto-created with factor=1.0 and no
  variant discriminator (applies to all variants)
- When a cross-category UoM is removed from uom_ids, the corresponding
  product.uom.factor record is deleted
- Adding a same-category UoM to uom_ids does not create a factor record
- When variants are assigned to a factor line but not all variants are
  covered, a no-discriminator (catch-all) line is preserved or re-created
  so that uncovered variants still have a conversion factor
"""

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestUC1ProductUomFactor(TransactionCase):
    """Test UC1: Product-Specific Cross-Category Conversion Factor"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.uom_ml = cls.env.ref("uom.product_uom_milliliter")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Ink - Cyan",
                "uom_id": cls.uom_gram.id,
            }
        )

    def test_factor_field_exists_with_default(self):
        """The factor field should exist on product.uom.factor and default
        to 1.0."""
        product_uom = self.env["product.uom.factor"].create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "uom_id": self.uom_ml.id,
            }
        )
        self.assertEqual(
            product_uom.factor,
            1.0,
            "The factor field should default to 1.0",
        )

    def test_product_ids_must_belong_to_same_template(self):
        """Assigning a variant from a different template should raise."""
        other_product = self.env["product.product"].create(
            {"name": "Other Product", "uom_id": self.uom_gram.id}
        )
        factor = self.env["product.uom.factor"].create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "uom_id": self.uom_ml.id,
            }
        )
        with self._assertRaises(ValidationError):
            factor.product_ids = [(4, other_product.id)]

    def test_same_category_factor_cannot_differ(self):
        """A packaging UoM in the same category as the product's base UoM
        should not allow a factor different from the standard UoM ratio.
        E.g. kg on a product with base UoM g must have factor = 1000."""
        uom_kg = self.env.ref("uom.product_uom_kgm")
        with self._assertRaises(Exception):
            self.env["product.uom.factor"].create(
                {
                    "product_tmpl_id": self.product.product_tmpl_id.id,
                    "uom_id": uom_kg.id,
                    "factor": 500.0,
                }
            )

    def test_same_category_factor_with_correct_ratio(self):
        """A same-category factor with the correct standard ratio should
        be accepted without error."""
        uom_kg = self.env.ref("uom.product_uom_kgm")
        factor = self.env["product.uom.factor"].create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "uom_id": uom_kg.id,
                "factor": uom_kg.factor / self.uom_gram.factor,
            }
        )
        self.assertTrue(factor)

    def test_auto_create_factor_on_cross_category_uom_add(self):
        """Adding a cross-category UoM to uom_ids should auto-create a
        product.uom.factor record with factor=1.0 and no discriminator."""
        template = self.product.product_tmpl_id
        template.uom_ids = [(4, self.uom_ml.id)]
        factor = self.env["product.uom.factor"].search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", self.uom_ml.id),
            ]
        )
        self.assertEqual(len(factor), 1)
        self.assertEqual(factor.factor, 1.0)
        self.assertFalse(factor.product_ids)

    def test_auto_delete_factor_on_cross_category_uom_remove(self):
        """Removing a cross-category UoM from uom_ids should delete the
        corresponding product.uom.factor record."""
        template = self.product.product_tmpl_id
        template.uom_ids = [(4, self.uom_ml.id)]
        factor = self.env["product.uom.factor"].search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", self.uom_ml.id),
            ]
        )
        self.assertEqual(len(factor), 1)
        template.uom_ids = [(3, self.uom_ml.id)]
        factor = self.env["product.uom.factor"].search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", self.uom_ml.id),
            ]
        )
        self.assertEqual(len(factor), 0)

    def test_same_category_uom_no_factor_created(self):
        """Adding a same-category UoM to uom_ids should not create a
        product.uom.factor record."""
        template = self.product.product_tmpl_id
        uom_kg = self.env.ref("uom.product_uom_kgm")
        template.uom_ids = [(4, uom_kg.id)]
        factor = self.env["product.uom.factor"].search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", uom_kg.id),
            ]
        )
        self.assertEqual(len(factor), 0)

    def test_catchall_line_when_not_all_variants_covered(self):
        """When a user assigns specific variants to a factor line but not
        all variants are covered, a no-discriminator catch-all line must
        exist so uncovered variants still have a conversion factor."""
        # Create a template with two variants
        attr = self.env["product.attribute"].create({"name": "Color"})
        val_red = self.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": attr.id}
        )
        val_blue = self.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": attr.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Test Ink",
                "uom_id": self.uom_gram.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr.id,
                            "value_ids": [(6, 0, [val_red.id, val_blue.id])],
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 2)
        variant_red = template.product_variant_ids[0]

        # Add cross-category UoM → creates catch-all factor line
        template.uom_ids = [(4, self.uom_ml.id)]
        factors = self.env["product.uom.factor"].search(
            [("product_tmpl_id", "=", template.id), ("uom_id", "=", self.uom_ml.id)]
        )
        self.assertEqual(len(factors), 1)
        catchall = factors.filtered(lambda f: not f.product_ids)
        self.assertEqual(len(catchall), 1)

        # Assign one variant to the existing line → should create a new
        # catch-all for the uncovered variant
        catchall.product_ids = [(4, variant_red.id)]
        factors = self.env["product.uom.factor"].search(
            [("product_tmpl_id", "=", template.id), ("uom_id", "=", self.uom_ml.id)]
        )
        self.assertEqual(len(factors), 2)
        new_catchall = factors.filtered(lambda f: not f.product_ids)
        self.assertEqual(
            len(new_catchall),
            1,
            "A catch-all line should exist for uncovered variants",
        )

    def test_catchall_recreated_on_discriminated_line_delete(self):
        """Deleting a discriminated factor line should re-create a catch-all
        if not all variants are still covered."""
        attr = self.env["product.attribute"].create({"name": "Size"})
        val_s = self.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": attr.id}
        )
        val_m = self.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": attr.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Test Ink",
                "uom_id": self.uom_gram.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr.id,
                            "value_ids": [(6, 0, [val_s.id, val_m.id])],
                        },
                    )
                ],
            }
        )
        variant_s, variant_m = template.product_variant_ids
        Factor = self.env["product.uom.factor"]

        # Add cross-category UoM → auto-creates catch-all
        template.uom_ids = [(4, self.uom_ml.id)]
        catchall = template.uom_factor_ids.filtered(
            lambda f: f.uom_id == self.uom_ml and not f.product_ids
        )
        self.assertEqual(len(catchall), 1)

        # Assign each variant to its own line, covering all variants
        catchall.product_ids = [(4, variant_s.id)]
        catchall.factor = 1.05
        f_s = catchall
        f_m = Factor.search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", self.uom_ml.id),
                ("id", "!=", f_s.id),
                ("product_ids", "=", False),
            ]
        )
        f_m.product_ids = [(4, variant_m.id)]
        f_m.factor = 1.10

        # Delete one → variant_m is no longer covered
        f_m.unlink()
        factors = Factor.search(
            [("product_tmpl_id", "=", template.id), ("uom_id", "=", self.uom_ml.id)]
        )
        catchall = factors.filtered(lambda f: not f.product_ids)
        self.assertEqual(
            len(catchall),
            1,
            "A catch-all should be re-created after deleting a discriminated line",
        )

    def test_duplicate_catchall_removed_when_variants_cleared(self):
        """Clearing product_ids on a discriminated line makes it a catch-all.
        If another catch-all already exists for the same (template, uom),
        the duplicate must be removed."""
        attr = self.env["product.attribute"].create({"name": "Finish"})
        val_a = self.env["product.attribute.value"].create(
            {"name": "Matte", "attribute_id": attr.id}
        )
        val_b = self.env["product.attribute.value"].create(
            {"name": "Gloss", "attribute_id": attr.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Test Ink",
                "uom_id": self.uom_gram.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr.id,
                            "value_ids": [(6, 0, [val_a.id, val_b.id])],
                        },
                    )
                ],
            }
        )
        variant_a = template.product_variant_ids[0]
        Factor = self.env["product.uom.factor"]

        # Auto-create catch-all via uom_ids
        template.uom_ids = [(4, self.uom_ml.id)]
        catchall = Factor.search(
            [
                ("product_tmpl_id", "=", template.id),
                ("uom_id", "=", self.uom_ml.id),
                ("product_ids", "=", False),
            ]
        )
        self.assertEqual(len(catchall), 1)

        # Assign a variant → creates a second catch-all for uncovered
        catchall.product_ids = [(4, variant_a.id)]
        factors = Factor.search(
            [("product_tmpl_id", "=", template.id), ("uom_id", "=", self.uom_ml.id)]
        )
        self.assertEqual(len(factors), 2)

        # Now clear the variant → this line becomes a catch-all again
        # The other catch-all must be removed to avoid duplicates
        discriminated = factors.filtered(lambda f: f.product_ids)
        discriminated.product_ids = [(5,)]
        factors = Factor.search(
            [("product_tmpl_id", "=", template.id), ("uom_id", "=", self.uom_ml.id)]
        )
        catchalls = factors.filtered(lambda f: not f.product_ids)
        self.assertEqual(
            len(catchalls),
            1,
            "Only one catch-all line should remain after clearing variants",
        )
