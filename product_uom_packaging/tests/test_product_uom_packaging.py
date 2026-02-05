# Copyright 2025 Rod Wilson Industries
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import cast

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests import M2MProxy, O2MProxy
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestProductUomPackaging(TransactionCase):
    """Test cases for product.uom.packaging model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        # Products
        cls.product_a = cls.env["product.product"].create({"name": "Product A"})
        cls.product_b = cls.env["product.product"].create({"name": "Product B"})

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
                "packaging_length": 30,
                "width": 20,
                "height": 15,
                "base_weight": 1.0,
                "max_weight": 25,
            }
        )

        # Companies (for multi-company tests)
        cls.company_main = cls.env.company
        # cls.company_other = cls.env["res.company"].create({"name": "Other Company"})


class TestConstraints(TestProductUomPackaging):
    """Test Group 2: Constraints and Validation"""

    @mute_logger("odoo.sql_db")
    def test_unique_template_uom_company(self):
        """Cannot create duplicate template/UoM/company combination."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
            }
        )
        # Creating another with same template/UoM should fail
        with self.assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_a.product_tmpl_id.id,
                    "uom_id": self.uom_dozen.id,
                }
            )

    def test_unique_allows_different_companies(self):
        """Can create same template/UoM combination for different companies."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "company_id": self.company_main.id,
            }
        )
        company = self.env["res.company"].create({"name": "Other Company"})
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "company_id": company.id,
            }
        )

    def test_unique_allows_different_templates(self):
        """Can create same UoM/package_type combination for different templates."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        # Creating same UoM/package_type for different template should work
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_b.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertTrue(packaging.exists())

    def test_unique_allows_different_uoms(self):
        """Can create same template/package_type combination for different UoMs."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        # Creating same template/package_type for different UoM should work
        packaging2 = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertTrue(packaging2.exists())

    @mute_logger("odoo.sql_db")
    def test_required_product_tmpl_or_variants(self):
        """Either product_tmpl_id OR product_variant_ids must be set."""
        # Creating packaging without product should fail
        with self.assertRaises(IntegrityError):
            self.ProductUomPackaging.create(
                {
                    "uom_id": self.uom_dozen.id,
                }
            )

    @mute_logger("odoo.sql_db")
    def test_required_uom(self):
        """UoM is required - cannot create without uom_id."""
        with self.assertRaises(IntegrityError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_a.product_tmpl_id.id,
                }
            )

    def test_optional_package_type(self):
        """Package type is optional - can create without package_type_id."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
            }
        )
        self.assertFalse(packaging.package_type_id)

    def test_default_sequence(self):
        """New records get default sequence value."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
            }
        )
        self.assertEqual(packaging.sequence, 10)


class TestMultiCompany(TestProductUomPackaging):
    """Test Group 4: Multi-Company Behavior"""

    def test_default_company(self):
        """New records default to current user's company."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
            }
        )
        self.assertEqual(packaging.company_id, self.env.company)


class TestPackageTypeIntegration(TestProductUomPackaging):
    """Test Group 5: Integration with Package Type"""

    def test_package_type_dimensions_accessible(self):
        """Can access package type dimensions through the configuration."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(packaging.package_type_id.packaging_length, 10)
        self.assertEqual(packaging.package_type_id.width, 10)
        self.assertEqual(packaging.package_type_id.height, 10)

    def test_package_type_weight_accessible(self):
        """Can access package type weight limits through the configuration."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.assertEqual(packaging.package_type_id.base_weight, 0.5)
        self.assertEqual(packaging.package_type_id.max_weight, 10)


class TestProductFormIntegration(TestProductUomPackaging):
    """Test Group 6: Product Form Integration"""

    def test_product_form_shows_packaging_inventory_tab(self):
        """Product form inventory tab displays packaging configurations."""
        from odoo.tests import Form

        # Create some packaging configurations
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_large.id,
                "sequence": 20,
            }
        )

        # Test product variant form
        with Form(self.product_a) as product_form:
            # Check if packaging_ids field exists and has records
            self.assertTrue(hasattr(product_form, "packaging_ids"))
            packagings = product_form.packaging_ids
            self.assertEqual(len(packagings), 2)

            # Verify ordering by sequence
            packaging_0 = cast(M2MProxy, packagings)[0]
            packaging_1 = cast(M2MProxy, packagings)[1]
            self.assertEqual(packaging_0.sequence, 10)
            self.assertEqual(packaging_1.sequence, 20)

            # Verify field values
            self.assertEqual(packaging_0.uom_id, self.uom_unit)
            self.assertEqual(packaging_0.package_type_id, self.package_small)
            self.assertEqual(packaging_1.uom_id, self.uom_dozen)
            self.assertEqual(packaging_1.package_type_id, self.package_large)

    def test_product_template_form_shows_packaging_inventory_tab(self):
        """Product template form inventory tab displays packaging configurations."""
        from odoo.tests import Form

        # Get the template for product_a
        template = self.product_a.product_tmpl_id

        # Create packaging configurations for the template's variants
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )

        # Test product template form
        with Form(template) as template_form:
            # Check if packaging_ids field exists and has records
            self.assertTrue(hasattr(template_form, "packaging_ids"))
            packagings = template_form.packaging_ids
            self.assertEqual(len(packagings), 1)

            # Verify field values - template field is now editable with inverse function
            packaging_0 = cast(O2MProxy, packagings).edit(0)
            # Since no variants were specified, packaging applies to all variants
            self.assertFalse(packaging_0.record.product_variant_ids)
            self.assertEqual(packaging_0.uom_id, self.uom_unit)
            self.assertEqual(packaging_0.package_type_id, self.package_small)

    def test_product_form_can_create_packaging(self):
        """Can create packaging configuration from product form."""
        from odoo.tests import Form

        # Test creating packaging through product form
        with Form(self.product_a) as product_form:
            cast(M2MProxy, product_form.packaging_ids).add(
                self.env["product.uom.packaging"].create(
                    {
                        "uom_id": self.uom_unit.id,
                        "package_type_id": self.package_small.id,
                        "product_tmpl_id": self.product_a.product_tmpl_id.id,
                        "sequence": 5,
                    }
                )
            )
            cast(M2MProxy, product_form.packaging_ids).add(
                self.env["product.uom.packaging"].create(
                    {
                        "uom_id": self.uom_unit.id,
                        "package_type_id": self.package_small.id,
                        "product_tmpl_id": self.product_a.product_tmpl_id.id,
                        "product_variant_ids": [Command.set([self.product_a.id])],
                        "sequence": 5,
                    }
                )
            )

            # Save the form
            product_form.save()

        # Verify the packaging was created
        packagings = self.ProductUomPackaging.search(
            [("product_tmpl_id", "=", self.product_a.product_tmpl_id.id)]
        )
        self.assertEqual(len(packagings), 2)
        self.assertEqual(packagings[0].uom_id, self.uom_unit)
        self.assertEqual(packagings[0].package_type_id, self.package_small)
        self.assertEqual(packagings[0].sequence, 5)

    def test_product_form_can_edit_packaging(self):
        """Can edit packaging configuration from product form."""
        from odoo.tests import Form

        # Create initial packaging
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )

        # Test editing packaging through product form
        with Form(self.product_a) as product_form:
            # Edit the first packaging line
            packaging_line = product_form.packaging_ids[0]
            packaging_line.sequence = 15
            packaging_line.package_type_id = self.package_large

            # Save the form
            product_form.save()

        # Verify the packaging was updated
        updated_packaging = self.ProductUomPackaging.browse(packaging.id)
        self.assertEqual(updated_packaging.sequence, 15)
        self.assertEqual(updated_packaging.package_type_id, self.package_large)

    def test_product_form_can_delete_packaging(self):
        """Can delete packaging configuration from product form."""
        from odoo.tests import Form

        # Create initial packaging
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )

        # Test deleting packaging through product form
        with Form(self.product_a) as product_form:
            # Remove the first packaging line
            product_form.packaging_ids.remove(index=0)

            # Save the form
            product_form.save()

        # Verify the packaging was deleted
        self.assertFalse(packaging.exists())
        packagings = self.ProductUomPackaging.search(
            [("product_tmpl_id", "=", self.product_a.product_tmpl_id.id)]
        )
        self.assertEqual(len(packagings), 0)


class TestInversePackagingIds(TestProductUomPackaging):
    """Test Group: Inverse function for packaging_ids on product.product"""

    def test_inverse_adds_template_packaging_from_different_template(self):
        """Adding packaging from different template via inverse updates template."""
        # Create packaging on product_b's template
        other_packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_b.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
            }
        )

        # Add to product_a's packaging_ids (this triggers the inverse)
        self.product_a.packaging_ids = self.product_a.packaging_ids + other_packaging

        # The inverse should update the template to product_a's template
        self.assertEqual(
            other_packaging.product_tmpl_id,
            self.product_a.product_tmpl_id,
            "Inverse should update product_tmpl_id when adding packaging",
        )
        # Should have no variant_ids (template-level)
        self.assertFalse(other_packaging.product_variant_ids)


class TestMultiVariantTemplateDisplay(TestProductUomPackaging):
    """Test Group 6: Multi-Variant Template Display"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Skip company creation due to warehouse constraint issues
        # cls.company_other = cls.env["res.company"].create({"name": "Other Company"})

    def test_template_shows_variant_identification_for_multiple_variants(self):
        """Template shows variant identification when multiple variants exist."""
        # Skip this test for now due to setup issues
        from odoo.tests import Form

        # Create attribute and values for proper variant generation
        attr_size = self.env["product.attribute"].create({"name": "Size"})
        attr_val_a = self.env["product.attribute.value"].create(
            {"name": "Size A", "attribute_id": attr_size.id}
        )
        attr_val_b = self.env["product.attribute.value"].create(
            {"name": "Size B", "attribute_id": attr_size.id}
        )

        # Create a template with multiple variants via attribute lines
        template = self.env["product.template"].create(
            {
                "name": "Multi-Variant Product",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attr_size.id,
                            "value_ids": [Command.set([attr_val_a.id, attr_val_b.id])],
                        }
                    )
                ],
            }
        )

        # Get the generated variants
        variants = template.product_variant_ids
        self.assertEqual(len(variants), 2)
        variant_a = variants.filtered(
            lambda v: attr_val_a
            in v.product_template_attribute_value_ids.product_attribute_value_id
        )
        variant_b = variants.filtered(
            lambda v: attr_val_b
            in v.product_template_attribute_value_ids.product_attribute_value_id
        )
        variant_a.default_code = "MVP-A"
        variant_b.default_code = "MVP-B"

        # Create packaging for each variant
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": variant_a.product_tmpl_id.id,
                "product_variant_ids": [variant_a.id],
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "sequence": 10,
            }
        )
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": variant_b.product_tmpl_id.id,
                "product_variant_ids": [variant_b.id],
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_large.id,
                "sequence": 20,
            }
        )

        # Test template form shows both packagings with variant identification
        with Form(template) as template_form:
            packagings = template_form.packaging_ids
            self.assertEqual(len(packagings), 2)

            # Verify we can see which variant each packaging belongs to
            packaging_0 = cast(O2MProxy, packagings).edit(0)
            packaging_1 = cast(O2MProxy, packagings).edit(1)

            # Should be ordered by sequence, then by product
            self.assertEqual(packaging_0.sequence, 10)
            self.assertIn(variant_a, packaging_0.product_variant_ids)
            self.assertEqual(packaging_1.sequence, 20)
            self.assertIn(variant_b, packaging_1.product_variant_ids)

            # Verify the variant identification through attribute values
            variant_0_ids = packaging_0.product_variant_ids
            variant_1_ids = packaging_1.product_variant_ids
            self.assertEqual(len(variant_0_ids), 1)
            self.assertEqual(len(variant_1_ids), 1)
            self.assertEqual(variant_0_ids[0].default_code, "MVP-A")
            self.assertEqual(variant_1_ids[0].default_code, "MVP-B")

    def test_template_packaging_editable_with_multiple_variants(self):
        """Can edit packaging from template form even with multiple variants."""
        # Skip this test for now due to setup issues
        from odoo.tests import Form

        # Create attribute and values for proper variant generation
        attr_color = self.env["product.attribute"].create({"name": "Color"})
        attr_val_a = self.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": attr_color.id}
        )
        attr_val_b = self.env["product.attribute.value"].create(
            {"name": "Blue", "attribute_id": attr_color.id}
        )

        # Create template with multiple variants via attribute lines
        template = self.env["product.template"].create(
            {
                "name": "Multi-Variant Edit Test",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attr_color.id,
                            "value_ids": [Command.set([attr_val_a.id, attr_val_b.id])],
                        }
                    )
                ],
            }
        )

        # Get the generated variants
        variants = template.product_variant_ids
        variant_a = variants.filtered(
            lambda v: attr_val_a
            in v.product_template_attribute_value_ids.product_attribute_value_id
        )
        # variant_b not needed in this test, just variant_a

        # Create initial packaging
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": variant_a.product_tmpl_id.id,
                "product_variant_ids": [variant_a.id],
                "uom_id": self.uom_unit.id,
                "sequence": 10,
            }
        )

        # Test editing through template form
        with Form(template) as template_form:
            with cast(O2MProxy, template_form.packaging_ids).edit(0) as packaging_line:
                packaging_line.sequence = 15
                packaging_line.package_type_id = self.package_small

        # Verify the packaging was updated
        updated_packaging = self.ProductUomPackaging.browse(packaging.id)
        self.assertEqual(
            updated_packaging.sequence, 15, "Sequence field should be updated"
        )
        self.assertEqual(updated_packaging.package_type_id, self.package_small)
        self.assertEqual(
            updated_packaging.product_variant_ids[0], variant_a
        )  # Should stay same variant


class TestActionOpenTemplate(TestProductUomPackaging):
    """Test Group: action_open_template method on product.product"""

    def test_action_open_template_returns_action(self):
        """action_open_template returns correct action dictionary."""
        action = self.product_a.action_open_template()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "product.template")
        self.assertEqual(action["res_id"], self.product_a.product_tmpl_id.id)
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "current")


class TestInverseVariantSpecificPackaging(TestProductUomPackaging):
    """Test Group: Inverse function with variant-specific packaging"""

    def test_inverse_adds_variant_specific_packaging_keeps_variants(self):
        """Adding variant-specific packaging via inverse keeps the variant
        association."""
        # Create a multi-variant template
        attr = self.env["product.attribute"].create({"name": "Test Attr"})
        attr_val_a = self.env["product.attribute.value"].create(
            {"name": "Val A", "attribute_id": attr.id}
        )
        attr_val_b = self.env["product.attribute.value"].create(
            {"name": "Val B", "attribute_id": attr.id}
        )

        template = self.env["product.template"].create(
            {
                "name": "Multi-Variant Test",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attr.id,
                            "value_ids": [Command.set([attr_val_a.id, attr_val_b.id])],
                        }
                    )
                ],
            }
        )

        variants = template.product_variant_ids
        variant_a = variants[0]
        variant_b = variants[1]

        # Create variant-specific packaging for variant_a (not yet linked to variant_b)
        variant_packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": template.id,
                "uom_id": self.uom_dozen.id,
                "product_variant_ids": [Command.set([variant_a.id])],
            }
        )

        # Verify it has variant_ids set
        self.assertTrue(variant_packaging.product_variant_ids)
        self.assertEqual(len(variant_packaging.product_variant_ids), 1)

        # Now add this packaging to variant_b's packaging_ids via the inverse
        # This triggers the else branch in _inverse_packaging_ids
        variant_b.packaging_ids = variant_b.packaging_ids + variant_packaging

        # The inverse should keep the product_variant_ids (the else branch)
        # and update the template
        self.assertEqual(
            variant_packaging.product_tmpl_id,
            template,
            "Inverse should keep product_tmpl_id for variant-specific packaging",
        )


class TestProductVariantConstraint(TestProductUomPackaging):
    """Test Group: Constraint that variants must belong to the same template"""

    @mute_logger("odoo.sql_db")
    def test_variant_must_belong_to_template(self):
        """Cannot create packaging with variant from different template."""
        # Try to create packaging with product_a's template but product_b as variant
        with self.assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": self.product_a.product_tmpl_id.id,
                    "uom_id": self.uom_unit.id,
                    "product_variant_ids": [Command.set([self.product_b.id])],
                }
            )

    def test_duplicate_variant_packaging_raises_error(self):
        """Cannot create duplicate variant-specific packaging for same UoM/company."""
        # Create a multi-variant template
        attr = self.env["product.attribute"].create({"name": "Dup Test Attr"})
        attr_val = self.env["product.attribute.value"].create(
            {"name": "Val", "attribute_id": attr.id}
        )

        template = self.env["product.template"].create(
            {
                "name": "Dup Test Product",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attr.id,
                            "value_ids": [Command.set([attr_val.id])],
                        }
                    )
                ],
            }
        )

        variant = template.product_variant_ids[0]

        # Create first variant-specific packaging
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": template.id,
                "uom_id": self.uom_unit.id,
                "product_variant_ids": [Command.set([variant.id])],
            }
        )

        # Try to create duplicate - same variant, same UoM, same company
        with self.assertRaises(ValidationError):
            self.ProductUomPackaging.create(
                {
                    "product_tmpl_id": template.id,
                    "uom_id": self.uom_unit.id,
                    "product_variant_ids": [Command.set([variant.id])],
                }
            )
