# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.tests.common import SavepointCase


class TestProductPricelistRevision(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist_obj = cls.env["product.pricelist"]
        cls.pricelist_item_obj = cls.env["product.pricelist.item"]
        cls.product_category_obj = cls.env["product.category"]
        cls.product_template_obj = cls.env["product.template"]
        cls.product_product_obj = cls.env["product.product"]
        # Create a price list, a product category, a product template and
        # a product variant
        cls.pricelist = cls.pricelist_obj.create(
            {"name": "Pricelist", "item_ids": False}
        )
        cls.product_category = cls.product_category_obj.create(
            {"name": "Product Category"}
        )
        cls.product_template = cls.product_template_obj.create(
            {"name": "Product Template", "categ_id": cls.product_category.id}
        )
        cls.product_product = cls.product_product_obj.create(
            {"name": "Product Variant", "categ_id": cls.product_category.id}
        )
        # Create pricelist items
        cls.pricelist_item_global = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "compute_price": "formula",
                "price_discount": 15,
            }
        )
        cls.pricelist_item_product_category = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": cls.product_category.id,
                "compute_price": "formula",
                "price_discount": 10,
            }
        )
        cls.pricelist_item_product_template = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_template.id,
                "compute_price": "percentage",
                "percent_price": 5,
            }
        )
        cls.pricelist_item_product_product = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": cls.product_product.id,
                "compute_price": "fixed",
                "fixed_price": 100,
            }
        )

    def test_search_name(self):
        item_obj = self.pricelist_item_obj
        result = item_obj.search([("name", "ilike", "product")])
        expected = self.pricelist_item_product_category
        expected |= self.pricelist_item_product_template
        expected |= self.pricelist_item_product_product
        self.assertEqual(result, expected)
        result = item_obj.search([("name", "ilike", "product category")])
        self.assertEqual(result, self.pricelist_item_product_category)
        result = item_obj.search([("name", "ilike", "product template")])
        self.assertEqual(result, self.pricelist_item_product_template)
        result = item_obj.search([("name", "ilike", "product variant")])
        self.assertEqual(result, self.pricelist_item_product_product)
        result = item_obj.search([("name", "ilike", "all")])
        self.assertEqual(len(result), 0)

    def test_wizard_action_apply_and_compute_variation_percent(self):
        wizard_obj = self.env["product.pricelist.item.duplicate.wizard"]
        # Before duplicate there are 4 items
        self.assertEqual(len(self.pricelist.item_ids), 4)
        items_before_wizard = self.pricelist.item_ids
        # Create wizard from pricelist_item_product_product and aply
        active_ids = self.pricelist_item_product_product.ids
        wizard = wizard_obj.with_context(active_ids=active_ids).create(
            {
                "date_start": date.today(),
                "date_end": date.today(),
                "variation_percent": 50,
            }
        )
        wizard.action_apply()
        # There will be one more item in self.pricelist
        self.assertEqual(len(self.pricelist.item_ids), 5)
        new_item = self.pricelist.item_ids - items_before_wizard
        self.assertEqual(new_item.previous_item_id.id, active_ids[0])
        self.assertEqual(new_item.previous_price, 100)
        self.assertEqual(new_item.fixed_price, 150)
        self.assertEqual(new_item.variation_percent, 50)
