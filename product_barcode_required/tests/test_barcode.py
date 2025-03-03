# Copyright 2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import exceptions
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class TestBarcodeDefault(BaseCommon):
    def test_barcode_is_not_required(self):
        self.assertFalse(self.env["product.template"]._is_barcode_required_enabled())
        self.assertFalse(self.env["product.product"]._is_barcode_required_enabled())

    def test_onchange_default_template(self):
        """Nothing changes since the constraint is not enabled."""
        form = Form(self.env["product.template"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertFalse(form.barcode)
        record = form.save()
        self.assertFalse(record.barcode)

    def test_onchange_default_variant(self):
        """Nothing changes since the constraint is not enabled."""
        form = Form(self.env["product.product"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertFalse(form.barcode)
        record = form.save()
        self.assertFalse(record.barcode)


class TestBarcodeTemplateRequired(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.product_variant_barcode_required = True
        cls.product_attribute = cls.env["product.attribute"].create(
            {"name": "Test Attribute"}
        )
        cls.product_attribute_value_1 = cls.env["product.attribute.value"].create(
            {
                "name": "Value 1",
                "attribute_id": cls.product_attribute.id,
            }
        )
        cls.product_attribute_value_2 = cls.env["product.attribute.value"].create(
            {
                "name": "Value 2",
                "attribute_id": cls.product_attribute.id,
            }
        )

    def test_barcode_is_required(self):
        self.assertTrue(self.env["product.template"]._is_barcode_required_enabled())
        self.assertTrue(self.env["product.product"]._is_barcode_required_enabled())

    def test_onchange_required_template(self):
        """Requirement enabled, default barcode to default_code."""
        form = Form(self.env["product.template"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertEqual(form.barcode, "PROD-A")
        record = form.save()
        self.assertEqual(record.barcode, "PROD-A")

    def test_required_template(self):
        """Requirement enabled, template needs it only if 1 variant is there."""
        tmpl = self.env["product.template"].create({"name": "Foo"})
        self.assertTrue(tmpl.is_barcode_required)
        # Add a variant
        self.env["product.product"].create(
            {
                "name": "another test variant",
                "barcode": "baz",
                "default_code": "yeah",
                "product_tmpl_id": tmpl.id,
            }
        )
        self.assertFalse(tmpl.is_barcode_required)

    def test_onchange_required_variant(self):
        """Requirement enabled, default barcode to default_code."""
        form = Form(self.env["product.product"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertEqual(form.barcode, "PROD-A")
        record = form.save()
        self.assertEqual(record.barcode, "PROD-A")

    def test_validation_create(self):
        """Cannot create a record w/out barcode as constraint is enabled."""
        with self.assertRaises(exceptions.ValidationError) as err:
            self.env["product.product"].create(
                [{"name": "Variant A"}, {"name": "Variant B"}, {"name": "Variant C"}]
            )
        self.assertEqual(
            err.exception.args[0],
            "These products have no barcode:"
            "\n\n  * Variant A\n  * Variant B\n  * Variant C",
        )
        # Defaults to default_code if not passed explicitly
        prod1 = self.env["product.product"].create(
            {"name": "Variant A", "default_code": "VAR-A"}
        )
        self.assertEqual(prod1.barcode, prod1.default_code)
        # pass it at creation, value is kept
        prod2 = self.env["product.product"].create(
            {"name": "Variant A", "default_code": "VAR-A", "barcode": "VAR-A-XYZ"}
        )
        self.assertEqual(prod2.barcode, "VAR-A-XYZ")

    def test_validation_write(self):
        """Cannot write a record w/out barcode as constraint is enabled."""
        prod = self.env["product.product"].create(
            {"name": "Variant A", "default_code": "VAR-A", "barcode": "VAR-A"}
        )
        # If you unset the barcode, it will be rolled back to default_code
        prod.barcode = False
        self.assertEqual(prod.barcode, "VAR-A")
        # Unless you unset both
        with self.assertRaises(exceptions.ValidationError) as err:
            prod.write({"default_code": False, "barcode": False})

        self.assertEqual(
            err.exception.args[0], "These products have no barcode:\n\n  * Variant A"
        )

    def test_create_variant_from_template(self):
        """Barcode does not propagate from template to variants."""
        with Form(self.env["product.template"]) as template_form:
            template_form.name = "Test Product"
            self.assertTrue(template_form.is_barcode_required)
            template_form.default_code = "TEST-PRODUCT"
            with template_form.attribute_line_ids.new() as line:
                line.attribute_id = self.product_attribute
                line.value_ids.add(self.product_attribute_value_1)
                line.value_ids.add(self.product_attribute_value_2)

        product_template = template_form.save()

        self.assertFalse(product_template.is_barcode_required)
        self.assertEqual(len(product_template.product_variant_ids), 2)

        for variant in product_template.product_variant_ids:
            self.assertEqual(len(variant.product_template_attribute_value_ids), 1)
            self.assertIn(
                variant.product_template_attribute_value_ids.product_attribute_value_id,
                [self.product_attribute_value_1, self.product_attribute_value_2],
            )
            self.assertFalse(variant.barcode)
            self.assertTrue(variant.is_barcode_required)

    def test_create_variant_from_template_barcode_error(self):
        """Variant created from template should have barcode set to default_code. ?"""
        with self.assertRaises(AssertionError):
            with Form(self.env["product.template"]) as template_form:
                template_form.name = "Test Product Raise Error"
                self.assertTrue(template_form.is_barcode_required)
