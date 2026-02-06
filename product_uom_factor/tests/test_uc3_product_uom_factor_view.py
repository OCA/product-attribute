"""
Test UC3: Cross-Category UoM Conversion Factors on Product Form

As a product manager, when I add a UoM from a different category to my
product's allowed UoMs, I want a "Unit Conversions" section to appear on
the product form showing which cross-category UoMs need conversion
factors, so that I can configure them without navigating away.

Conversion factors are stored in product.uom.factor records linked to the
product template (product_tmpl_id), with an optional product_ids M2M to
restrict to specific variants.

Acceptance Criteria:
- The product template form has a "Unit Conversions" section (under the
  Inventory tab) showing the uom_factor_ids one2many with uom_id (readonly),
  product_ids, and factor columns
- Factor lines are auto-created when cross-category UoMs are added to
  uom_ids; the factor field is editable inline
- The uom_id column is readonly since lines are auto-managed
"""

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestUC3ProductUomFactorView(TransactionCase):
    """Test UC3: Cross-Category UoM Conversion Factors on Product Form"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.config.settings"].create({"group_uom": True}).execute()
        cls.uom_gram = cls.env.ref("uom.product_uom_gram")
        cls.uom_ml = cls.env.ref("uom.product_uom_milliliter")

    def test_factor_editable_on_template_form(self):
        """When a cross-category UoM is added to uom_ids, the auto-created
        factor line appears on the template form and its factor can be
        edited inline."""
        template = self.env["product.template"].create(
            {
                "name": "Test Ink",
                "uom_id": self.uom_gram.id,
            }
        )
        # Add cross-category UoM → auto-creates factor line
        template.uom_ids = [(4, self.uom_ml.id)]
        self.assertEqual(len(template.uom_factor_ids), 1)

        # Open form and edit the factor value
        form = Form(template, view="product.product_template_only_form_view")
        with form.uom_factor_ids.edit(0) as line:
            line.factor = 1.05
        template = form.save()
        puom = template.uom_factor_ids.filtered(lambda r: r.uom_id == self.uom_ml)
        self.assertEqual(len(puom), 1)
        self.assertAlmostEqual(
            puom.factor,
            1.05,
            places=5,
            msg="Factor should be editable via the product template form",
        )

    def test_variant_uom_factor_ids_shows_applicable_factors(self):
        """The computed uom_factor_ids on product.product should return
        only factors that apply to this variant: catch-all lines (no
        product_ids) and lines where this variant is in product_ids."""
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
        variant_red, variant_blue = template.product_variant_ids

        # Add cross-category UoM → catch-all factor
        template.uom_ids = [(4, self.uom_ml.id)]
        catchall = template.uom_factor_ids
        self.assertEqual(len(catchall), 1)

        # Both variants see the catch-all
        self.assertEqual(variant_red.uom_factor_ids, catchall)
        self.assertEqual(variant_blue.uom_factor_ids, catchall)

        # Discriminate: assign red variant → catch-all re-created for blue
        catchall.product_ids = [(4, variant_red.id)]
        catchall.factor = 1.10
        template.invalidate_recordset(["uom_factor_ids"])
        factors = template.uom_factor_ids
        red_line = factors.filtered(lambda f: variant_red in f.product_ids)
        new_catchall = factors.filtered(lambda f: not f.product_ids)

        # Red sees its discriminated line + catch-all
        variant_red.invalidate_recordset(["uom_factor_ids"])
        variant_blue.invalidate_recordset(["uom_factor_ids"])
        self.assertEqual(variant_red.uom_factor_ids, red_line | new_catchall)
        # Blue sees only the catch-all
        self.assertEqual(variant_blue.uom_factor_ids, new_catchall)

        # Verify via variant form view
        form = Form(variant_red, view="product.product_normal_form_view")
        self.assertEqual(len(form.uom_factor_ids), 2)
        form = Form(variant_blue, view="product.product_normal_form_view")
        self.assertEqual(len(form.uom_factor_ids), 1)

    def test_new_product_uom_factor_ids_empty(self):
        """A new (unsaved) product should return empty uom_factor_ids."""
        new_product = self.env["product.product"].new({"name": "Unsaved"})
        self.assertFalse(new_product.uom_factor_ids)
