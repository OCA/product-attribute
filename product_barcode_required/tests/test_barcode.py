# Copyright 2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import exceptions
from odoo.tests import Form, SavepointCase


class TestBarcodeBase(SavepointCase):

    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))


class TestBarcodeDefault(TestBarcodeBase):
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


class TestBarcodeTemplateRequired(TestBarcodeBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.product_variant_barcode_required = True

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
        # Add a variantc
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
            err.exception.name,
            "These products have no barcode:"
            "\n\n  * Variant A\n  * Variant B\n  * Variant C",
        )
        # Defaults to default_code if not passed explicitely
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
            err.exception.name, "These products have no barcode:\n\n  * Variant A"
        )

    # TODO: test variant create from template
