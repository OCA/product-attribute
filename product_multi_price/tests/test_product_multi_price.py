# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductMultiPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.price_name_obj = cls.env["product.multi.price.name"]
        cls.price_field_1 = cls.price_name_obj.create({"name": "test_field_1"})
        cls.price_field_2 = cls.price_name_obj.create({"name": "test_field_2"})
        prod_tmpl_obj = cls.env["product.template"]
        cls.prod_1 = prod_tmpl_obj.create(
            {
                "name": "Test Product Template",
                "price_ids": [
                    Command.create({"name": cls.price_field_1.id, "price": 5.5}),
                    Command.create({"name": cls.price_field_2.id, "price": 20.0}),
                ],
            }
        )
        cls.prod_att_1 = cls.env["product.attribute"].create({"name": "Color"})
        cls.prod_attr1_v1 = cls.env["product.attribute.value"].create(
            {"name": "red", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_attr1_v2 = cls.env["product.attribute.value"].create(
            {"name": "blue", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_2 = prod_tmpl_obj.create(
            {
                "name": "Test Product 2 With Variants",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.prod_att_1.id,
                            "value_ids": [
                                Command.set(
                                    [cls.prod_attr1_v1.id, cls.prod_attr1_v2.id]
                                )
                            ],
                        },
                    )
                ],
            }
        )
        cls.prod_prod_2_1 = cls.prod_2.product_variant_ids[0]
        cls.prod_prod_2_2 = cls.prod_2.product_variant_ids[1]
        cls.prod_prod_2_1.write(
            {
                "price_ids": [
                    Command.create({"name": cls.price_field_1.id, "price": 6.6}),
                    Command.create({"name": cls.price_field_2.id, "price": 7.7}),
                ],
            }
        )
        cls.prod_prod_2_2.write(
            {
                "price_ids": [
                    Command.create({"name": cls.price_field_1.id, "price": 8.8}),
                    Command.create({"name": cls.price_field_2.id, "price": 9.9}),
                ],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": cls.price_field_1.id,
                            "price_discount": 10,
                            "display_applied_on": "1_product",
                        },
                    )
                ],
            }
        )

    def test_product_multi_price_pricelist(self):
        """Pricelists based on multi prices for templates or variants"""
        price = self.prod_1.with_context(
            pricelist=self.pricelist.id
        )._get_contextual_price()
        self.assertAlmostEqual(price, 4.95)
        price = self.prod_prod_2_1.with_context(
            pricelist=self.pricelist.id
        )._get_contextual_price()
        self.assertAlmostEqual(price, 5.94)
        price = self.prod_prod_2_2.with_context(
            pricelist=self.pricelist.id
        )._get_contextual_price()
        self.assertAlmostEqual(price, 7.92)

    def test_product_multi_price_pricelist_item(self):
        """Pricelists based on multi prices using the pricelist items"""
        pricelist_item = self.pricelist.item_ids[0]
        today = fields.Date.context_today(self.env.user)
        price = pricelist_item._compute_price(
            self.prod_1,
            1.0,
            self.prod_1.uom_id,
            today,
        )
        self.assertAlmostEqual(price, 4.95)
        price = pricelist_item._compute_price(
            self.prod_prod_2_1,
            1.0,
            self.prod_prod_2_1.uom_id,
            today,
        )
        self.assertAlmostEqual(price, 5.94)
        price = pricelist_item._compute_price(
            self.prod_prod_2_2,
            1.0,
            self.prod_prod_2_2.uom_id,
            today,
        )
        self.assertAlmostEqual(price, 7.92)

    def test_create_multi_price_name_without_company(self):
        """Test creating a multi price name without company_id"""
        # Create a multi price name without company - explicitly set to False
        # to bypass default
        price_name = self.price_name_obj.create(
            {"name": "test_global_field_new", "company_id": False}
        )
        self.assertFalse(price_name.company_id)
        self.assertEqual(price_name.name, "test_global_field_new")

    def test_create_multi_price_name_with_company(self):
        """Test creating a multi price name with company_id"""
        company = self.env.ref("base.main_company")
        price_name = self.price_name_obj.create(
            {"name": "test_company_field", "company_id": company.id}
        )
        self.assertTrue(price_name.company_id)
        self.assertEqual(price_name.company_id, company)

    def test_multi_price_name_uniqueness_constraint(self):
        """Test that names must be unique per company"""
        company = self.env.ref("base.main_company")

        # Create first one with company using a highly unique name to avoid conflicts
        import time
        import uuid

        # Generate a unique name with validation to avoid any potential conflicts
        attempt = 0
        while True:
            unique_suffix = str(uuid.uuid4()).replace("-", "")[:8]
            timestamp_ns = time.time_ns() + attempt
            test_method = self._testMethodName[:10]
            unique_name = f"unique_name_{test_method}_{timestamp_ns}_{unique_suffix}"

            # Check if the name already exists in the database
            existing = self.env["product.multi.price.name"].search(
                [("name", "=", unique_name)], limit=1
            )

            if not existing:
                break
            attempt += 1  # Try with different timestamp

        self.price_name_obj.create({"name": unique_name, "company_id": company.id})

        # Try to create another with same name and company - should fail
        # We expect an integrity error, so we can temporarily disable the
        # logger to keep the test log clean.
        import logging

        sql_db_logger = logging.getLogger("odoo.sql_db")
        original_level = sql_db_logger.level
        sql_db_logger.setLevel(logging.CRITICAL)
        try:
            with self.assertRaises(ValidationError), self.env.cr.savepoint():
                self.price_name_obj.create(
                    {"name": unique_name, "company_id": company.id}
                )
        finally:
            sql_db_logger.setLevel(original_level)

        # But creating with different company should work
        company2 = self.env["res.company"].create(
            {
                "name": f"Test Company 2_{self._testMethodName[:20]}",
                "currency_id": self.env.ref("base.EUR").id,
            }
        )
        # Create a different unique name for second company
        attempt2 = 0
        while True:
            unique_suffix2 = str(uuid.uuid4()).replace("-", "")[:8]
            timestamp_ns2 = time.time_ns() + attempt2
            test_method2 = self._testMethodName[:10]
            unique_name2 = (
                f"unique_name2_{test_method2}_{timestamp_ns2}_{unique_suffix2}"
            )

            # Check if the name already exists in the database
            existing2 = self.env["product.multi.price.name"].search(
                [("name", "=", unique_name2)], limit=1
            )

            if not existing2:
                break
            attempt2 += 1  # Try with different timestamp

        self.price_name_obj.create({"name": unique_name2, "company_id": company2.id})

    def test_multi_price_name_without_company_can_repeat(self):
        """Test that names without company can be repeated (though not recommended)"""
        # Create multi price names without company to avoid conflicts
        import time
        import uuid

        unique_suffix = str(uuid.uuid4()).replace("-", "")[
            :12
        ]  # Longer UUID without dashes for uniqueness
        timestamp_ns = time.time_ns()  # Nanosecond precision for maximum uniqueness
        unique_name = (
            f"global_name_{self._testMethodName}_{timestamp_ns}_{unique_suffix}"
        )
        name1 = self.price_name_obj.create({"name": unique_name, "company_id": False})
        name2 = self.price_name_obj.create(
            {"name": unique_name, "company_id": False}
        )  # Should work
        self.assertEqual(name1.name, name2.name)
        self.assertFalse(name1.company_id)
        self.assertFalse(name2.company_id)

    def test_product_multi_price_creation(self):
        """Test creating multi prices for products"""
        product = self.env["product.product"].create({"name": "Test Product"})

        # Create multi price
        multi_price = self.env["product.multi.price"].create(
            {
                "name": self.price_field_1.id,
                "product_id": product.id,
                "price": 15.0,
            }
        )

        self.assertEqual(multi_price.name, self.price_field_1)
        self.assertEqual(multi_price.product_id, product)
        self.assertEqual(multi_price.price, 15.0)

    def test_multi_price_company_propagation(self):
        """Test that multi price inherits company from multi price name"""
        company = self.env.ref("base.main_company")
        price_name_with_company = self.price_name_obj.create(
            {"name": "test_with_company", "company_id": company.id}
        )

        product = self.env["product.product"].create({"name": "Test Product"})

        multi_price = self.env["product.multi.price"].create(
            {
                "name": price_name_with_company.id,
                "product_id": product.id,
                "price": 25.0,
            }
        )

        self.assertEqual(multi_price.company_id, company)

    def test_pricelist_item_multi_price_integration(self):
        """Test pricelist item with multi price base"""
        # Create a new pricelist item with multi_price base
        pricelist_item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "compute_price": "formula",
                "base": "multi_price",
                "multi_price_name": self.price_field_2.id,
                "price_discount": 5,
            }
        )

        self.assertEqual(pricelist_item.base, "multi_price")
        self.assertEqual(pricelist_item.multi_price_name, self.price_field_2)
        self.assertEqual(pricelist_item.price_discount, 5)

    def test_get_multiprice_pricelist_price(self):
        """Test getting multiprice from pricelist item"""
        # Create a pricelist rule using the second price field
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist 2",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": self.price_field_2.id,
                            "price_discount": 10,
                        }
                    )
                ],
            }
        )

        # Calculate price using the pricelist
        price = self.prod_1.with_context(pricelist=pricelist.id)._get_contextual_price()

        # Price should be 20.0 (from price_field_2) with 10% discount = 18.0
        self.assertAlmostEqual(price, 18.0)

    def test_multiprice_without_company_usage(self):
        """Test using multi price names without company assigned"""
        # Create a multi price name without company
        global_price_name = self.price_name_obj.create({"name": "global_price"})

        # Assign this to a product
        self.env["product.multi.price"].create(
            {
                "name": global_price_name.id,
                "product_id": self.prod_1.product_variant_ids[0].id,
                "price": 100.0,
            }
        )

        # Create a pricelist that uses this global price
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Global Price Test",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": global_price_name.id,
                            "price_discount": 0,
                        }
                    )
                ],
            }
        )

        # The price should reflect the global price
        price = self.prod_1.with_context(pricelist=pricelist.id)._get_contextual_price()

        self.assertEqual(price, 100.0)

    def test_constraint_unique_per_company(self):
        """Test that multi prices are unique per name and company"""
        company = self.env.ref("base.main_company")

        # Create a multi price name with company
        price_name = self.price_name_obj.create(
            {"name": "unique_test", "company_id": company.id}
        )

        product1 = self.env["product.product"].create({"name": "Product 1"})
        product2 = self.env["product.product"].create({"name": "Product 2"})

        # Create multi price for first product
        self.env["product.multi.price"].create(
            {
                "name": price_name.id,
                "product_id": product1.id,
                "price": 10.0,
            }
        )

        # Create multi price for second product with same name and company - should work
        multi_price2 = self.env["product.multi.price"].create(
            {
                "name": price_name.id,
                "product_id": product2.id,
                "price": 20.0,
            }
        )

        self.assertTrue(multi_price2.exists())

    def test_compute_name_text(self):
        """Test the name_text field computation"""
        product = self.env["product.product"].create({"name": "Test Product"})

        multi_price = self.env["product.multi.price"].create(
            {
                "name": self.price_field_1.id,
                "product_id": product.id,
                "price": 30.0,
            }
        )

        # name_text should be the same as the name field's name
        self.assertEqual(multi_price.name_text, self.price_field_1.name)

    def test_multi_price_template_integration(self):
        """Test multi price integration with product templates"""
        # Check that the price_ids are properly computed for templates
        # prod_2 has variants
        # prod_prod_2_1 is one of the variants

        # When template has only one variant, price_ids should be linked
        single_variant_template = self.env["product.template"].create(
            {
                "name": "Single Variant Template",
                "price_ids": [
                    Command.create({"name": self.price_field_1.id, "price": 42.0})
                ],
            }
        )

        # The template should have the same price_ids as its single variant
        self.assertEqual(len(single_variant_template.price_ids), 1)
        self.assertEqual(single_variant_template.price_ids.price, 42.0)

    def test_multiprice_pricelist_price_calculation(self):
        """Test detailed calculation of multiprice in pricelist context"""
        # Create detailed pricelist with surcharge and margins
        pricelist_with_details = self.env["product.pricelist"].create(
            {
                "name": "Detailed Calculation Test",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": self.price_field_1.id,
                            "price_discount": 10,  # 10% discount
                            "price_surcharge": 5,  # +5 surcharge
                            "price_min_margin": 2,  # minimum 2 margin
                            "price_max_margin": 20,  # maximum 20 margin
                            "price_round": 0.01,
                        }
                    )
                ],
            }
        )

        # For prod_1, price_field_1 is 5.5
        # Calculation:
        # price_limit = 5.5
        # price = 5.5 - (5.5 * 0.10) = 4.95
        # price is not rounded here as it matches rounding
        # price = 4.95 + 5 (surcharge) = 9.95
        # price = max(9.95, 5.5 + 2) = max(9.95, 7.5) = 9.95
        # price = min(9.95, 5.5 + 20) = min(9.95, 25.5) = 9.95
        calculated_price = self.prod_1.with_context(
            pricelist=pricelist_with_details.id
        )._get_contextual_price()
        self.assertAlmostEqual(calculated_price, 9.95)

    def test_multi_price_uniqueness_constraint(self):
        """Test multi_price uniqueness constraint per company."""
        product = self.env["product.product"].create({"name": "Test Product"})
        self.env["product.multi.price"].create(
            {
                "name": self.price_field_1.id,
                "product_id": product.id,
                "price": 10.0,
            }
        )
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.env["product.multi.price"].create(
                {
                    "name": self.price_field_1.id,
                    "product_id": product.id,
                    "price": 20.0,
                }
            )

    def test_pricelist_item_ondelete(self):
        """Test that when a multi.price.name is deleted, the corresponding
        pricelist item's multi_price_name is set to default (null)"""
        pricelist_item = self.env["product.pricelist.item"].create(
            {
                "compute_price": "formula",
                "base": "multi_price",
                "multi_price_name": self.price_field_1.id,
            }
        )
        self.price_field_1.unlink()
        # Reload the record to see the updated value after unlinking the related record
        pricelist_item.invalidate_recordset(["multi_price_name"])
        # Access the field again to reload from DB
        updated_multi_price_name = (
            self.env["product.pricelist.item"]
            .browse(pricelist_item.id)
            .multi_price_name
        )
        self.assertFalse(updated_multi_price_name)

    def test_product_without_multiprice(self):
        """Test that a product without a specific multi-price returns a price of 0"""
        product_no_price = self.env["product.template"].create(
            {"name": "Product without multi-price"}
        )
        price = product_no_price.with_context(
            pricelist=self.pricelist.id
        )._get_contextual_price()
        self.assertEqual(price, 0)

    def test_template_with_multiple_variants(self):
        """Test that a template with multiple variants does not have price_ids
        and returns 0 for multiprice"""
        self.assertFalse(self.prod_2.price_ids)
        price = self.prod_2._get_multiprice_pricelist_price(self.pricelist.item_ids[0])
        self.assertEqual(price, 0)

    def test_default_get_company(self):
        """Test the default `_get_company` method."""
        # Test without company in context
        price_name_no_company = self.price_name_obj.create({"name": "No company"})
        self.assertFalse(price_name_no_company.company_id)

        # Test with company in context
        company = self.env.ref("base.main_company")
        price_name_with_company = self.price_name_obj.with_context(
            company_id=company.id
        ).create({"name": "With company"})
        self.assertEqual(price_name_with_company.company_id, company)

    def test_pricelist_not_multi_price(self):
        """Test that the computation doesn't fail for non multi price rules."""
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test not multi price",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "fixed_price": 5,
                        }
                    )
                ],
            }
        )
        price = self.prod_1.with_context(pricelist=pricelist.id)._get_contextual_price()
        self.assertEqual(price, 5)

    def test_price_compute_multi_price(self):
        """Test _price_compute with multi_price type."""

        prices = self.prod_1._price_compute("multi_price")

        self.assertEqual(prices[self.prod_1.id], 1.0)
