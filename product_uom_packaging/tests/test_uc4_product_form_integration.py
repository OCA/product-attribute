"""
Test UC4: Product Form Integration

As a product manager, I want to see and manage packaging configurations
on the product form's inventory tab
so that I can manage all packaging settings from one place.

Acceptance Criteria:
- Template form shows packaging_ids as editable inline list
- Can create template-level and variant-specific packaging via form
- Variant form shows packaging_ids (read-only)
- Inverse updates product_tmpl_id when adding packaging
- action_open_template navigates to the template form
"""

from typing import cast

from odoo.fields import Command
from odoo.tests import Form, O2MProxy
from odoo.tests.common import TransactionCase


class TestUC4ProductFormIntegration(TransactionCase):
    """Test UC4: Product Form Integration"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        cls.product_a = cls.env["product.product"].create({"name": "Product A"})
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
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

    def _create_multi_variant_template(self):
        """Helper to create a template with Small/Large variants."""
        attr_size = self.env["product.attribute"].create({"name": "Size"})
        val_small = self.env["product.attribute.value"].create(
            {"name": "Small", "attribute_id": attr_size.id}
        )
        val_large = self.env["product.attribute.value"].create(
            {"name": "Large", "attribute_id": attr_size.id}
        )
        template = self.env["product.template"].create(
            {
                "name": "Multi-Variant Product",
                "uom_id": self.uom_unit.id,
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": attr_size.id,
                            "value_ids": [Command.set([val_small.id, val_large.id])],
                        }
                    )
                ],
            }
        )
        return template

    def test_product_form_shows_packaging_ids(self):
        """UC4: Product variant form exposes packaging_ids."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(self.product_a) as f:
            self.assertEqual(len(f.packaging_ids), 1)

    def test_template_form_shows_packaging_ids(self):
        """UC4: Product template form exposes packaging_ids as editable list."""
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(self.product_a.product_tmpl_id) as f:
            self.assertEqual(len(f.packaging_ids), 1)

    def test_template_form_can_create_packaging(self):
        """UC4: Can create packaging inline on the template form."""
        template = self._create_multi_variant_template()

        with Form(template) as f:
            with cast(O2MProxy, f.packaging_ids).new() as line:
                line.uom_id = self.uom_dozen
                line.qty = 12.0
                line.package_type_id = self.package_large
            f.save()

        packaging = self.ProductUomPackaging.search(
            [("product_tmpl_id", "=", template.id)]
        )
        self.assertEqual(len(packaging), 1)
        self.assertFalse(packaging.product_variant_ids)

    def test_template_form_can_create_variant_specific_packaging(self):
        """UC4: Can create variant-specific packaging inline on the template form."""
        template = self._create_multi_variant_template()
        variant_small = template.product_variant_ids[0]

        with Form(template) as f:
            with cast(O2MProxy, f.packaging_ids).new() as line:
                line.uom_id = self.uom_unit
                line.package_type_id = self.package_small
                line.product_variant_ids.add(variant_small)
            f.save()

        packaging = self.ProductUomPackaging.search(
            [("product_tmpl_id", "=", template.id)]
        )
        self.assertEqual(packaging.product_variant_ids, variant_small)

    def test_template_form_shows_variant_identification(self):
        """UC4: Template form shows variant_ids for variant-scoped packaging."""
        template = self._create_multi_variant_template()
        variant_small = template.product_variant_ids[0]

        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": template.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
                "name": "Small Box (All)",
            }
        )
        self.ProductUomPackaging.create(
            {
                "product_tmpl_id": template.id,
                "product_variant_ids": [Command.set([variant_small.id])],
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_large.id,
            }
        )

        with Form(template) as f:
            self.assertEqual(len(f.packaging_ids), 2)
            line_0 = cast(O2MProxy, f.packaging_ids).edit(0)
            self.assertFalse(line_0.product_variant_ids)
            line_1 = cast(O2MProxy, f.packaging_ids).edit(1)
            self.assertTrue(line_1.product_variant_ids)

    def test_product_form_can_delete_packaging(self):
        """UC4: Can delete packaging from the product form."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(self.product_a) as f:
            f.packaging_ids.remove(index=0)
            f.save()
        self.assertFalse(packaging.exists())

    def test_inverse_updates_template(self):
        """UC4: Inverse updates product_tmpl_id when adding packaging."""
        product_b = self.env["product.product"].create({"name": "Product B"})
        other_packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": product_b.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        self.product_a.packaging_ids = self.product_a.packaging_ids + other_packaging
        self.assertEqual(
            other_packaging.product_tmpl_id, self.product_a.product_tmpl_id
        )

    def test_inverse_updates_template_for_variant_specific_packaging(self):
        """UC4: Inverse sets product_tmpl_id for variant-specific packaging
        without clearing product_variant_ids."""
        template = self._create_multi_variant_template()
        variant_small = template.product_variant_ids[0]
        variant_large = template.product_variant_ids[1]

        # Create packaging scoped to variant_large on this template
        variant_packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": template.id,
                "product_variant_ids": [Command.set([variant_large.id])],
                "uom_id": self.uom_dozen.id,
                "package_type_id": self.package_large.id,
            }
        )

        # Directly assign it into variant_small's packaging_ids.
        # variant_packaging is NOT in variant_small.variant_packaging_ids,
        # but it HAS product_variant_ids set, so the inverse else branch fires.
        variant_small.packaging_ids = variant_small.packaging_ids + variant_packaging

        # The inverse should have set product_tmpl_id without clearing
        # product_variant_ids (the else branch).
        self.assertEqual(variant_packaging.product_tmpl_id, template)
        self.assertTrue(variant_packaging.product_variant_ids)

    def test_action_open_template(self):
        """UC4: action_open_template returns correct action."""
        action = self.product_a.action_open_template()
        self.assertEqual(action["res_model"], "product.template")
        self.assertEqual(action["res_id"], self.product_a.product_tmpl_id.id)
